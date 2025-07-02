# Use official Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy backend code
COPY backend/ ./backend/
COPY backend/requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy frontend
COPY frontend/ ./frontend/

# Expose Flask port
EXPOSE 5000

# Start the Flask app
CMD ["python", "./backend/app.py"]
