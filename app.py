from google.cloud import storage
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
from flask_sqlalchemy import SQLAlchemy
from keras.models import load_model
from models.userModel import User, db
import pytesseract
import numpy as np
import re
import os
import uvicorn
import download


app = Flask(__name__)

port = int(os.getenv("PORT"))

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Configuration SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_CONNECTIONS")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# db.init_app(app)
# Configuration Google Cloud Storage
BUCKET_NAME = 'ember-donor'
BUCKET_FOLDER = 'userprofile'

# Path to service account JSON file
service_account_path = os.getenv("GCP_CREDENTIALS")

# Create Google Cloud Storage client using service account JSON file
storage_client = storage.Client.from_service_account_json(service_account_path)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_image_to_bucket(filename):
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(f'{BUCKET_FOLDER}/{filename}')
    blob.upload_from_filename(os.path.join(UPLOAD_FOLDER, filename))

def preprocess_image(image):
    image = image.resize((512, 512))  # Resize image to (512, 512) pixels
    image = np.array(image)  # Convert PIL Image to NumPy array
    image = image / 255.0 
    return image

def postprocess_predictions(predictions):
    threshold = 0.5
    bounding_boxes = []
    for prediction in predictions:
        if prediction > threshold:
            bounding_boxes.append(prediction)
    return bounding_boxes


def extract_text_within_boxes(image, bounding_boxes):
    extracted_text = []
    for box in bounding_boxes:
        cropped_image = image.crop(box)  # Crop image based on bounding box
        text = pytesseract.image_to_string(
            cropped_image)  # Apply OCR to cropped image
        extracted_text.append(text)
    return extracted_text


def process_ktp(filename):
    try:
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)

        model = load_model('bounding_ktp03.h5')
        processed_image = preprocess_image(image)
        predictions = model.predict(np.expand_dims(processed_image, axis=0))
        bounding_boxes = postprocess_predictions(predictions)
        extracted_text = extract_text_within_boxes(image, bounding_boxes)

        return extracted_text

    except Exception as e:
        return str(e)


def extract_data(text_data):
    name_pattern = r'Name:\s+(.*)'
    gender_pattern = r'Gender:\s+(.*)'

    name_match = re.search(name_pattern, text_data)
    gender_match = re.search(gender_pattern, text_data)

    name = name_match.group(1) if name_match else 'Not found'
    gender = gender_match.group(1) if gender_match else 'Not found'

    return name, gender


def update_user_profile(name, gender):
    user_profile = User.query.first()
    user_profile.name = name
    user_profile.gender = gender
    db.session.commit()


@app.route('/upload-ktp', methods=['PATCH'])
def upload_ktp():
    if 'file' not in request.files:
        return jsonify({'message': 'No file uploaded'}), 400

    file = request.files['file']
    if not allowed_file(file.filename):
        return jsonify({'message': 'Invalid file extension'}), 400

    filename = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    upload_image_to_bucket(filename)
    text_data = process_ktp(filename)
    name, gender = extract_data(text_data)
    update_user_profile(name, gender)

    return jsonify({'name': name, 'gender': gender}), 200

if __name__ == '__main__':
    app.run(debug=True)
    download.run()
    uvicorn.run(app, host="0.0.0.0", port=port, timeout_keep_alive=1200)
