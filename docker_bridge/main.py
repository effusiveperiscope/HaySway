from flask import Flask, request, jsonify, abort, send_file
from werkzeug.utils import secure_filename
import requests
import os
from pathlib import Path

APP_PORT = 7802

app = Flask(__name__)

# We cannot use RAW_DIR unless we are planning to match Hay Say's metadata.

# Mapping of archs to internal and port
arch_to_destination = {
    "controllable_talknet": 6574,
    "so_vits_svc_3": 6575,
    "so_vits_svc_4": 6576,
    "so_vits_svc_5": 6577,
    "rvc": 6578,
}

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    arch = data.get('architecture', None)

    if arch not in arch_to_destination:
        return jsonify({'error': 'Invalid architecture'}), 400

    destination_port = arch_to_destination[arch]
    url = f"http://0.0.0.0:{destination_port}"

    # Forward the request to the internal IP and port
    response = requests.post(url, json=data)

    return jsonify({'response': response.json()})

@app.route('/upload_raw', methods=['POST'])
def upload_raw():
    from hay_say_common import character_dir, AUDIO_FOLDER
    HAY_SWAY_RAW_DIR = os.path.join(AUDIO_FOLDER,"hay_sway_raw")

    if 'audio_file' not in request.files:
        return 'No audio file part'

    file = request.files['audio_file']
    filename = secure_filename(Path(file).name)
    file_path = os.path.join(HAY_SWAY_RAW_DIR, filename)
    file.save(os.path.join(HAY_SWAY_RAW_DIR, filename))
    return jsonify({'saved_file': file.filename})

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    from hay_say_common import character_dir, AUDIO_FOLDER
    HAY_SWAY_OUT_DIR = os.path.join(AUDIO_FOLDER,"hay_sway_out")

    file_path = os.path.join(HAY_SWAY_OUT_DIR, filename)
    if not os.path.exists(file_path):
        return abort(404)
    return send_file(file_path)

@app.route('/info', methods = ['GET'])
def info():
    from hay_say_common import character_dir, AUDIO_FOLDER
    HAY_SWAY_RAW_DIR = os.path.join(AUDIO_FOLDER,"hay_sway_raw")
    HAY_SWAY_OUT_DIR = os.path.join(AUDIO_FOLDER,"hay_sway_out")

    return jsonify({
        'HAY_SWAY_RAW_DIR': HAY_SWAY_RAW_DIR,
        'HAY_SWAY_OUT_DIR': HAY_SWAY_OUT_DIR
        })

@app.route('/available_characters', methods=['GET'])
def available_characters():
    data = request.get_json()
    arch = data.get('architecture', None)

    if arch is None:
        return jsonify({'error': 'Invalid architecture'}), 400

    characters = os.listdir(characters_dir(arch))

    return jsonify({'characters': characters})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=APP_PORT)
