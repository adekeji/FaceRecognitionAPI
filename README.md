# Face Recognition API & Kubernetes Tutorial

This repository now provides both the original Face Recognition API and a comprehensive Kubernetes bare metal installation tutorial website.

## Features

### Original API
- Face detection and recognition using advanced computer vision
- RESTful API endpoints for image processing
- Support for JPEG and PNG images

### Kubernetes Tutorial (NEW!)
- Complete step-by-step guide for Kubernetes bare metal installation
- Interactive web interface with progress tracking
- Copy-paste code snippets for all commands
- Responsive design for mobile and desktop
- Troubleshooting section with common issues and solutions

## Quick Start

### Option 1: Tutorial Server (Lightweight - No Dependencies)
For just the Kubernetes tutorial website:

```bash
python3 kubernetes_server.py
```

Visit: http://localhost:8000/kubernetes-tutorial

### Option 2: Full API (Requires Dependencies)
For both face recognition API and tutorial:

```bash
pip install -r requirements.txt
python3 main.py
```

Visit: 
- http://localhost:8000/ (API)
- http://localhost:8000/kubernetes-tutorial (Tutorial)

## API Endpoints

- `GET /` - API information and tutorial link
- `GET /health` - Health check
- `GET /kubernetes-tutorial` - Interactive Kubernetes installation tutorial
- `POST /detect-faces` - Face detection in uploaded images (requires dependencies)

## Tutorial Features

### Interactive Elements
- ✅ Progress tracking with localStorage
- 📋 Copy-to-clipboard functionality for code blocks
- 📱 Responsive design for all devices
- 🎯 Smooth navigation between sections
- ⚠️ Command validation warnings
- 💡 Helpful tips and notes

### What You'll Learn
- Bare metal server preparation
- Kubernetes control plane setup
- Worker node configuration
- Network plugin installation (Flannel/Calico)
- Cluster verification and testing
- Common troubleshooting scenarios

## Directory Structure

```
.
├── main.py                 # Original FastAPI application
├── kubernetes_server.py    # Lightweight tutorial server
├── static/
│   ├── css/
│   │   └── style.css      # Tutorial styling
│   └── js/
│       └── tutorial.js    # Interactive functionality
├── requirements.txt        # Python dependencies
├── startup.sh             # Deployment script
└── README.md              # This file
```

## Kubernetes Prerequisites

### Hardware Requirements
- **Control Plane:** 2+ CPU cores, 2GB+ RAM, 20GB+ storage
- **Worker Nodes:** 1+ CPU cores, 1GB+ RAM, 10GB+ storage
- **Network:** Full connectivity between all nodes

### Software Requirements
- Ubuntu 20.04+ / CentOS 7+ / RHEL 7+ / Debian 9+
- Container runtime (containerd/Docker)
- Required ports open (6443, 10250, etc.)

## Development

### Running in Development Mode
```bash
# Tutorial only (no dependencies)
python3 kubernetes_server.py 8000

# Full application with face recognition
pip install fastapi uvicorn
python3 main.py
```

### Deployment
The application is configured for deployment on Azure, Heroku, or any cloud platform supporting Python web applications.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source. Please see the license file for details.

---

**Note:** The face recognition functionality requires additional system dependencies (dlib, OpenCV) which may take time to install. For just the Kubernetes tutorial, use `kubernetes_server.py` which requires no external dependencies.