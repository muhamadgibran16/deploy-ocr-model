# Base image
FROM python:3.10.2

# Set working directory
WORKDIR /app

RUN pip install --upgrade pip

# Copy requirements.txt
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy application files
COPY . .

# Expose the application port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the application
CMD gunicorn -b :$PORT app:app
