## Deployment OCR API - Machine Learning Model

This endpoint is used to receive input in the form of an ID card image, then process it with a model, and return the output as text, which includes the name and gender data. The data is then saved in a database, and the ID card image is stored in a non-public cloud storage.

Deployment process:

- Prepare a GitHub repository for the API project.

- Configure the API deployment settings using a Dockerfile, including specifying the required dependencies, source code, and runtime environment:
```
# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

RUN pip install --upgrade pip

# Install build tools
RUN apt-get update && apt-get install -y build-essential

# Install system-level dependencies
RUN apt-get update && apt-get install -y default-libmysqlclient-dev libgl1-mesa-glx tesseract-ocr

RUN apt-get install -y tesseract-ocr-eng

# Copy requirements.txt
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy application files
COPY . .

# Expose the application port
EXPOSE 5000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
```
- Create a repository secret for environment variables such as project ID, service account, database configuratiion, and other sensitive data.
   
- Create a GitHub Actions workflow file named ```.github/workflows/main.yml``` to automate the deployment process.
   
Specify the necessary steps to build and deploy the API to Cloud Run and set up the required authentication and access permissions for the GitHub Actions workflow to interact with Cloud Run:
- Define the workflow trigger condition ```on```.
- Define the jobs to be executed ```jobs```.
- Specify the operating system to be used ```runs-on: ubuntu-latest```
- Set environment variables.
- Perform Google Cloud login ```google-github-actions/setup-gcloud```
- Configure Docker authorization ```gcloud auth configure-docker --quiet```
- Checkout the Repository ```actions/checkout```
- Build the Docker Image ```docker build -t $IMAGE_NAME .```
- Push the image to the Container Registry ```docker push $IMAGE_NAME```
- Deploy the Image to Cloud Run ```gcloud run deploy```

Push the changes to the GitHub repository to trigger the workflow and initiate the deployment process.

By following this deployment process, the endpoint can efficiently receive an ID card image, extract the required data, securely store the image in a non-public cloud storage, and provide the extracted information as output while maintaining data privacy and security.


Noted : [ocr model running on : https://github.com/muhamadgibran16/deploy-ocr-model](https://github.com/muhamadgibran16/deploy-ocr-model)
