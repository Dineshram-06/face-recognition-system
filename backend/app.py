from flask import Flask, request, jsonify, send_from_directory, render_template
import os
from werkzeug.utils import secure_filename
from face_utils import load_encodings, find_matches, save_encodings, create_encodings
import uuid

app = Flask(__name__, static_folder="../frontend/static", template_folder="../frontend")

UPLOAD_FOLDER = os.path.join(app.static_folder, "uploads")
MATCHED_FOLDER = os.path.join(app.static_folder, "matched")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_FOLDER = os.path.join(BASE_DIR, "dataset", "event_photos")
PKL_PATH = os.path.join(BASE_DIR, "encodings.pkl")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MATCHED_FOLDER, exist_ok=True)

# Load or generate encodings
if not os.path.exists(PKL_PATH):
    print("Generating encodings...")
    save_encodings(DATASET_FOLDER, PKL_PATH)
known_encodings, known_paths = load_encodings(PKL_PATH)


@app.route("/")
def index():
    return send_from_directory(app.template_folder, "index.html")


@app.route("/static/<path:path>")
def serve_static(path):
    return send_from_directory(app.static_folder, path)


@app.route("/api/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    tolerance = float(request.form.get("tolerance", 0.45))

    filename = str(uuid.uuid4()) + ".jpg"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    matches = find_matches(filepath, known_encodings, known_paths, tolerance)

    match_urls = []
    for match in matches:
        basename = os.path.basename(match)
        dest = os.path.join(MATCHED_FOLDER, basename)
        if not os.path.exists(dest):
            os.system(
                f'copy "{match}" "{dest}"'
                if os.name == "nt"
                else f'cp "{match}" "{dest}"'
            )
        match_urls.append(f"/static/matched/{basename}")

    return jsonify({"matches": match_urls})


if __name__ == "__main__":
    app.run(debug=True)
