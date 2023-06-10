# Base image
FROM python:3.10.2

# Set working directory
WORKDIR /app

RUN pip install --upgrade pip

# Copy requirements.txt
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y tesseract-ocr

# Copy application files
COPY . .

# Expose the application port
EXPOSE 5000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the application
# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]