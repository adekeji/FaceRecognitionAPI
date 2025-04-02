#!/bin/bash

# Update and install system dependencies required for dlib and face-recognition
echo "Installing system dependencies..."
apt update
apt install -y build-essential cmake libopenblas-dev liblapack-dev libx11-dev libgtk-3-dev libboost-python-dev python3-dev

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install uvicorn
pip install python-multipart
pip install -r requirements.txt

# Start the FastAPI application using Gunicorn
echo "Starting FastAPI application..."
#gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 main:app
gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:${PORT:-8080} main:app
#!/bin/bash
#gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT main:app
