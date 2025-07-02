FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libgl1-mesa-glx && apt-get clean

COPY app/ ./app/
COPY frontend/ ./frontend/

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["python", "app/app.py"]
