from http.client import HTTPConnection
from docker_bridge.main import APP_PORT
from recorder import RECORD_DIR
from pathlib import Path
import requests
import os
import config
import base64
import json

def extract_message(response):
    json_response = json.loads(response.content.decode('utf-8'))
    base64_encoded_message = json_response['message']
    return base64.b64decode(base64_encoded_message).decode('utf-8')

class VCInterface:
    OUTPUT_PATH = "results"

    def __init__(self):
        os.makedirs(VCInterface.OUTPUT_PATH, exist_ok=True)
        os.makedirs(RECORD_DIR, exist_ok=True)

        if not config.OFFLINE_DEBUG_MODE:
            self.vc_info = requests.get(
                'http://127.0.0.1:'+str(APP_PORT)+'/info').json()

    def input(self, options : dict, user_text : str, user_file_path : str,
              output_filename_cb):
        # user_file is on local side
        if user_file_path is not None:
            with open(user_file_path, 'rb') as user_file:
                response = requests.post('http://127.0.0.1:'+str(APP_PORT)+
                    '/upload_raw', files = {
                    'audio_file': (user_file_path, user_file)})
                saved_file = response.json()['saved_file']
        else:
            saved_file = ""

        # Gets the filename Path().name
        output_filename = output_filename_cb(saved_file)

        # Ignoring preprocessing/postprocessing for now
        payload = {
            'architecture': options['Architecture'],
            'Inputs': {
                'User Text': user_text,
                'User Audio': saved_file
            },
            'Options': options,
            'Output File': output_filename
        }
        
        response = requests.post('http://127.0.0.1:'+str(APP_PORT)+'/generate',
            headers={'Content-Type': 'application/json'}, json=payload)
        code = response.status_code
        if code != 200:
            print(extract_message(response))
            raise Exception("Docker bridge returned non-200 error code "+
                str(code))

        response = requests.get('http://127.0.0.1:'+str(APP_PORT)+'/download/'+
            output_filename)
        output_path = str(os.path.join(VCInterface.OUTPUT_PATH,
           output_filename))

        stem = Path(output_path).stem
        suffix = self.vc_info['CACHE_EXTENSION']

        i = 0
        while os.path.exists(output_path):
            output_path = stem+f"{i}"+suffix
            i += 1

        with open(
            os.path.join(VCInterface.OUTPUT_PATH,
                output_filename), 'wb') as file:
            file.write(response.content)

        return output_path
