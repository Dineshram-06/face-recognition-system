import face_recognition
import pickle
import os
from tqdm import tqdm
from operator import itemgetter
import numpy as np


def create_encodings(folder_path):
    encodings = []
    image_paths = []

    for filename in tqdm(os.listdir(folder_path), desc="Encoding faces"):
        path = os.path.join(folder_path, filename)
        image = face_recognition.load_image_file(path)
        face_locations = face_recognition.face_locations(image, model="cnn")
        face_encs = face_recognition.face_encodings(image, face_locations)

        for enc in face_encs:
            encodings.append(enc)
            image_paths.append(path)

    return encodings, image_paths


def save_encodings(folder_path, pkl_path):
    existing_encodings = []
    existing_paths = []

    # Load existing encodings if the file exists
    if os.path.exists(pkl_path):
        with open(pkl_path, "rb") as f:
            existing_encodings, existing_paths = pickle.load(f)

    # Get already processed file names
    processed_filenames = set(os.path.basename(path) for path in existing_paths)

    # Now only encode NEW images
    new_encodings = []
    new_paths = []

    for filename in tqdm(os.listdir(folder_path), desc="Checking new images"):
        if filename in processed_filenames:
            continue

        path = os.path.join(folder_path, filename)
        image = face_recognition.load_image_file(path)
        face_locations = face_recognition.face_locations(image, model="cnn")
        face_encs = face_recognition.face_encodings(image, face_locations)

        for enc in face_encs:
            new_encodings.append(enc)
            new_paths.append(path)

    print(f"[INFO] New faces encoded: {len(new_encodings)}")

    # Combine old + new
    all_encodings = existing_encodings + new_encodings
    all_paths = existing_paths + new_paths

    with open(pkl_path, "wb") as f:
        pickle.dump((all_encodings, all_paths), f)

    print(f"[INFO] Updated encodings saved to {pkl_path}")


def load_encodings(pkl_path):
    with open(pkl_path, "rb") as f:
        return pickle.load(f)


def find_matches(image_path, known_encodings, known_paths, tolerance=0.45):
    print(f"[INFO] Matching with tolerance = {tolerance}")
    unknown_image = face_recognition.load_image_file(image_path)
    locations = face_recognition.face_locations(unknown_image, model="cnn")
    encodings = face_recognition.face_encodings(unknown_image, locations)

    matched_files_with_distance = []

    for enc in encodings:
        distances = face_recognition.face_distance(known_encodings, enc)

        for i, dist in enumerate(distances):
            if dist <= tolerance:
                matched_files_with_distance.append((known_paths[i], dist))

    # 🌟 Eliminate duplicates — keep only the best match for each photo
    unique_matches = {}
    for path, dist in matched_files_with_distance:
        if path not in unique_matches or dist < unique_matches[path]:
            unique_matches[path] = dist

    # Sort the unique matches by distance (closest match first)
    sorted_matches = sorted(unique_matches.items(), key=itemgetter(1))

    return [path for path, _ in sorted_matches]
