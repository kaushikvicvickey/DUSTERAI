import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, jsonify
from core.detector import DustParticleEngine

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Reject files larger than 16MB

detector = DustParticleEngine()

def is_valid_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error="No image submitted.")
        
        file = request.files['file']
        if not file or file.filename == '':
            return render_template('index.html', error="No file selected.")
            
        if not is_valid_file(file.filename):
            return render_template('index.html', error="Invalid extension. Upload PNG, JPG, or WEBP.")

        filename = secure_filename(file.filename)
        raw_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(raw_path)

        try:
            metrics = detector.analyze(raw_path, app.config['UPLOAD_FOLDER'])
            return render_template('index.html', metrics=metrics, original=filename)
        except Exception as err:
            return render_template('index.html', error=f"Analysis failure: {str(err)}")

    return render_template('index.html')

@app.route('/api/v1/inspect', methods=['POST'])
def api_inspect():
    if 'file' not in request.files:
        return jsonify({"error": "Missing 'file' multipart field"}), 400
    
    file = request.files['file']
    if not is_valid_file(file.filename):
        return jsonify({"error": "Unsupported file format"}), 422

    filename = secure_filename(file.filename)
    raw_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(raw_path)

    metrics = detector.analyze(raw_path, app.config['UPLOAD_FOLDER'])
    return jsonify({
        "status": "success",
        "particle_count": metrics.total_particles,
        "mean_size_px": metrics.mean_particle_size_px,
        "classification": metrics.surface_contamination_index,
        "artifact_url": f"/static/uploads/{metrics.annotated_image_filename}"
    }), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
