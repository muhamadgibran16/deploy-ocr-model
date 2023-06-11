# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

RUN pip install --upgrade pip

# Copy requirements.txt
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y libgl1-mesa-glx

RUN apt-get update && apt-get install -y tesseract-ocr

# Copy application files
COPY . .

# Expose the application port
EXPOSE 5000

# Set environment variables
# ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]