from PyQt5.QtWidgets import (QComboBox)
import requests

APP_PORT = 7802

class CharacterDropdown(QComboBox):
    def __init__(self, arch):
        super().__init__()
        self.characters = []

        response = requests.get(f'http://0.0.0.0:{APP_PORT}',
            json={'architecture': arch})
        if response.status_code != 200:
            raise Exception("Non-200 status code for character dropdown: "
                +response.status_code)
        self.characters = response.json['characters']

        for c in self.characters:
            self.addItem(c)
