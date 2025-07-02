# Use official Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (CMake, g++, make, dlib dependencies)
RUN apt-get update && \
    apt-get install -y cmake g++ make libopenblas-dev liblapack-dev libx11-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy backend
COPY backend/ ./backend/
COPY backend/requirements.txt ./

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy frontend
COPY frontend/ ./frontend/

# Expose port
EXPOSE 5000

# Run the app
CMD ["python", "./backend/app.py"]
