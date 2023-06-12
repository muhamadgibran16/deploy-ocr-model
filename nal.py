import os
import traceback
import tensorflow as tf
from flask import Flask, request, jsonify
from pydantic import BaseModel


# Register the custom object
# custom_objects = {'KerasLayer': tf.keras.layers.KerasLayer}

# Initialize Model
# model = tf.keras.models.load_model('./model.h5', custom_objects=custom_objects)
# model = tf.saved_model.load("./model")


# # Initialize Model
# model = tf.keras.models.load_model('model.h5')
# model = tf.keras.models.load_model('./model.h5')
# model = tf.keras.models.load_model('model.h5')


app = Flask(__name__)

# This endpoint is for a test to this server


@app.route("/")
def index():
    return "Hello world from ML endpoint!"

# endpoint


class RequestText(BaseModel):
    text: str


@app.route("/predict_text", methods=["POST"])
def predict_text():
    try:
        req = request.get_json()
        text = req["text"]
        print("Uploaded text:", text)

        # Text preprocessing
        def preprocess_text(text):
            processed_text = text.lower()
            return processed_text

        # Prepare data for the model
        def prepare_data(input_data):
            prepared_data = [preprocess_text(data) for data in input_data]
            return prepared_data

        # Predict the data
        class ClassificationModel:
            def _init_(self, model):
                self.model = model

            def predict(self, input_data):
                input_data = tf.constant(input_data)
                predictions = self.model.predict(input_data)
                return predictions.tolist()

        # Create an instance of the model
        model = ClassificationModel(model)

        # Prepare the input data
        input_data = [text]
        prepared_data = prepare_data(input_data)

        # Predict the data
        result = model.predict(prepared_data)

        # Change the result to your desired API output
        def format_output(result):
            output = [{"text": data, "label": pred}
                      for data, pred in zip(input_data, result)]
            return output

        # Format the result to API output
        output = format_output(result)

        # Print the output
        print(output)

        return jsonify({"result": output})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# Starting the server
# Check the API documentation easily using /docs after the server is running

if __name__ == '__main__':
    app.run(debug=True)