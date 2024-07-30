# Base image
FROM python:3

# Set working directory
WORKDIR /app

# Add model file from GCS
ADD https://storage.googleapis.com/donorgo-bucket/model/bounding_ktp03.h5 /app

# Upgrade pip
RUN pip install --upgrade pip

# Install build tools
RUN apt-get update && apt-get install -y build-essential

# Install system-level dependencies
RUN apt-get update && apt-get install -y default-libmysqlclient-dev libgl1-mesa-glx tesseract-ocr

# Install tesseract-ocr-eng
RUN apt-get install -y tesseract-ocr-eng

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application files
COPY . .

# Expose the application port
EXPOSE 5000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000", "--log-level", "debug"]
