<img width="1280" height="640" alt="git (1)" src="https://github.com/user-attachments/assets/8920b256-2ba8-4988-b824-5351134eb4bd" />



# DUSTER-AI


## Basic Details
### Team Name: KAUSHIK KS'S team


### Team Members
- Team Lead: [Name] - College of Engneering, Alappuzha

### Project Description
An automated computer vision platform built with Flask and OpenCV that quantifies 
surface dust contamination on electronic displays without specialized hardware sensors.

### The Problem (that doesn't exist)
Proving scientifically that wiping a glossy screen with the hem of your hoodie doesn't actually clean anything
### The Solution (that nobody asked for)
Stray cat hairs and screen scratches get kicked out at the door

## Technical Details
### Technologies/Components Used
For Software:
- Python,HTML5,CSS3 & Bash / Shell
- Flask,OpenCV,Tailwind CSS & Gunicorn
- NumPy,Werkzeug,Dataclasses & Typing,OS
- Ubuntu Linux,systemd,Python venv & Pip

### Implementation
For Software:Multipart Payload Parsing,Payload Constraints
Filename Sanitization,MIME/Extension Verification
# Installation
sudo apt update && sudo apt install -y python3 python3-pip python3-venv libgl1 libglib2.0-0 curl
mkdir -p ~/dust_analyzer/core ~/dust_analyzer/static/uploads ~/dust_analyzer/templates
cd ~/dust_analyzer
touch core/__init__.py
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install Flask opencv-python-headless numpy gunicorn Werkzeug
pip list
chmod 755 ~/dust_analyzer/static/uploads
python3 -c "import cv2, flask, numpy; print('Environment verification successful: OpenCV', cv2.__version__)"
python3 app.py
pip install --upgrade pip
pip install Flask opencv-python-headless numpy gunicorn Werkzeug
python3 app.py
gunicorn -w 3 -b 127.0.0.1:5000 app:app

# Run
cd ~/dust_analyzer
source venv/bin/activate
python3 app.py

### Project Documentation
For Software:
[![Platform](https://img.shields.io/badge/Platform-Ubuntu%2022.04%20%7C%2024.04%20LTS-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)](https://ubuntu.com/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8%2B-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0%2B-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

## Key Features
* **Zero-Hardware Dependency**: Runs optical surface metrology using standard smartphone or webcam captures without dedicated laser particle counters.
* **Illumination-Invariant Morphology**: Uses **White Top-Hat transforms** and **CLAHE** to extract micro-particles while ignoring screen glare and uneven room shadows.
* **Geometric Feature Gating**: Filters artifacts by circularity ($4\pi \frac{\text{Area}}{\text{Perimeter}^2}$) and pixel surface area to reject scratches, screen bezels, and textile fibers.
* **Telemetry HUD Dashboard**: Features a responsive dark-mode UI with side-by-side raw/overlay comparisons and ISO-grade contamination grading.
* **Headless REST API**: Supports programmatic integration for mobile diagnostic tools, automated pipelines, or CLI scripts.
* **Production-Grade Architecture**: Includes Gunicorn multi-worker concurrency, Nginx reverse proxy buffering, and systemd process management.

## Project Structure
dust_analyzer/
├── core/
│   ├── __init__.py
│   └── detector.py            
├── static/
│   └── uploads/               
├── templates/
│   └── index.html             
├── app.py                     
├── dust_analyzer.service      
├── requirements.txt           
└── README.md
## Prerequisites
Operating System: Ubuntu 20.04, 22.04, or 24.04 LTS
Python: python3 (v3.10 or higher) and python3-pip, python3-venv
System Libraries: libgl1, libglib2.0-0 (required by OpenCV headless)
## Quick Start
git clone [https://github.com/kaushikvicvickey/DUSTERAI.git]
cd dust_analyzer
sudo apt update && sudo apt install -y python3-pip python3-venv libgl1 libglib2.0-0
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python3 app.py
sudo nano /etc/systemd/system/dust_analyzer.service
After=network.target
User=kaushikvicvickey
Group=www-data
WorkingDirectory=/home/kaushikvicvickey/dust_analyzer
Environment="PATH=/home/kaushikvicvickey/dust_analyzer/venv/bin"

# Screenshots (Add at least 3)
<img width="2816" height="1536" alt="ss" src="https://github.com/user-attachments/assets/432f5821-e9fc-41e5-826e-8b2c5394ae11" />

active deployment environment on the Ubuntu desktop. An active GNOME Terminal window is running the Gunicorn WSGI server from within the (venv) virtual environment, executing the specific production command

<img width="2816" height="1536" alt="ss1" src="https://github.com/user-attachments/assets/88fc621a-f295-4a64-b7bb-d2a91c7cfe0c" />

<img width="1973" height="1217" alt="ss2" src="https://github.com/user-attachments/assets/8ad72f4a-d945-4225-a746-49baf47c150f" />


# Diagrams
Input Image (Screen Off + Oblique Light)
   │
   ▼
[ Grayscale Conversion ] ────────────► Reduces 3-channel BGR to 1-channel luminance
   │
   ▼
[ CLAHE Normalization ] ─────────────► Equalizes local contrast variations (8x8 tiles)
   │
   ▼
[ White Top-Hat Transform ] ─────────► Isolates bright peaks narrower than 15x15 px
   │
   ▼
[ Otsu Dynamic Thresholding ] ───────► Separates foreground specks from background
   │
   ▼
[ Morphological Opening ] ───────────► Drops isolated single-pixel camera noise
   │
   ▼
[ Contour & Circularity Gating ] ────► Filters by compactness (C >= 0.35) and size (3-300 px²)
   │
   ▼
[ Telemetry & HUD Annotation ] ──────► Computes mean size, particle count, and rating

Made with ❤️ at TinkerHub Useless Projects 

![Static Badge](https://img.shields.io/badge/TinkerHub-24?color=%23000000&link=https%3A%2F%2Fwww.tinkerhub.org%2F)
![Static Badge](https://img.shields.io/badge/UselessProjects--26-26?link=https%3A%2F%2Ftinkerhub.org%2Fevents%2F1M8ORET9A1%2Fuseless-projects-3.0)



Ee sanathil changes varuthi GitHub readme ayite add akanam @all ennale projects approve agu ene ariyichitonde
