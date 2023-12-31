from flask import Flask, request, jsonify, abort, send_file
from werkzeug.utils import secure_filename
import requests
import os
from pathlib import Path
from logging.config import dictConfig
import soundfile as sf
#a

APP_PORT = 7802

dictConfig({
    'version': 1,
    'root': {
        'level': 'INFO'
    }
})

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

#@app.errorhandler(Exception)
#def handle_exception(e):
#    print(e)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    arch = data.get('architecture', None)

    if arch not in arch_to_destination:
        return jsonify({'error': 'Invalid architecture'}), 400

    destination_port = arch_to_destination[arch]
    url = "http://"+arch+"_server:"+f"{destination_port}/generate"

    # Remove otherwise breaks validation
    final_payload = data
    final_payload.pop('architecture', None)
    data.pop('architecture', None)

    # Forward the request to the internal IP and port
    response = requests.post(url, headers={'Content-Type':
        'application/json'}, json=final_payload)

    return response.content, response.status_code

@app.route('/upload_raw', methods=['POST'])
def upload_raw():
    from hay_say_common import (characters_dir, AUDIO_FOLDER,
        CACHE_FORMAT, CACHE_EXTENSION, PREPROCESSED_DIR)

    if 'audio_file' not in request.files:
        return 'No audio file part'

    file = request.files['audio_file']
    filename = Path(secure_filename(Path(file.filename).name)).stem
    file_path = os.path.join(PREPROCESSED_DIR, filename)+CACHE_EXTENSION

    try:
        data, sr = sf.read(file)
        sf.write(file_path, data, sr, format=CACHE_FORMAT)
    except Exception as e:
        app.logger.error("Error during conversion: ",str(e))

    return jsonify({'saved_file': file_path})

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    from hay_say_common import (characters_dir, AUDIO_FOLDER,
        OUTPUT_DIR, CACHE_EXTENSION)

    file_path = os.path.join(OUTPUT_DIR, filename)+CACHE_EXTENSION
    app.logger.info(file_path)
    if not os.path.exists(file_path):
        return 'No audio file found at '+str(filename), 404
    return send_file(file_path)

@app.route('/info', methods = ['GET'])
def info():
    from hay_say_common import characters_dir, AUDIO_FOLDER, CACHE_EXTENSION

    return jsonify({
        'CACHE_EXTENSION': CACHE_EXTENSION
        })

@app.route('/available_characters', methods=['GET'])
def available_characters():
    from hay_say_common import characters_dir, AUDIO_FOLDER
    data = request.get_json()
    arch = data.get('architecture', None)

    if arch is None:
        return jsonify({'error': 'Invalid architecture'}), 400

    characters = os.listdir(characters_dir(arch))

    return jsonify({'characters': characters})

if __name__ == '__main__':
    app.config['DEBUG']=True
    app.run(host='0.0.0.0', port=APP_PORT)
