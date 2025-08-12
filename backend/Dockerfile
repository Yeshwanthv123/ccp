# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app/backend

# Install system dependencies for cryptography
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libssl-dev \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install dependencies
# Note: The path is relative to the project root, not the Dockerfile itself
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend application code
COPY backend/. .

# Expose port 8000 for the FastAPI application
EXPOSE 8000

# Command to run the application
CMD ["python", "start.py"]