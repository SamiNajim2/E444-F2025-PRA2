# Small official Python image
FROM python:3.13-slim

# No buffering in logs
ENV PYTHONUNBUFFERED=1

# Workdir inside the image
WORKDIR /app

# Install dependencies first (cache-friendly)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Flask config for container
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000

# Start the app
CMD ["flask", "run"]
