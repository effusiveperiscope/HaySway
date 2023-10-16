from PyQt5.QtCore import (QSize)
from PyQt5.QtWidgets import (QFrame, QLineEdit, QLabel, QHBoxLayout, QCheckBox,
    QComboBox, QSizePolicy)
import unicodedata
import re

class NumField(QFrame):
    def __init__(self, label : str, default : str, validator):
        super().__init__()

        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(4)

        self.label = QLabel(label)
        self.layout.addWidget(self.label)

        self.field = QLineEdit(default)
        self.field.setValidator(validator)
        self.layout.addWidget(self.field)
        self.field.setSizePolicy(QSizePolicy.Maximum,
            QSizePolicy.Preferred)

    @property
    def value(self):
        return self.field.text()

class BoolField(QFrame):
    def __init__(self, label : str, default : bool = False):
        super().__init__()

        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(4)

        self.label = QLabel(label)
        self.layout.addWidget(self.label)

        self.field = QCheckBox()
        self.field.setCheckState(default)
        self.layout.addWidget(self.field)
        self.field.setSizePolicy(QSizePolicy.Maximum,
            QSizePolicy.Preferred)

    @property
    def value(self):
        return self.field.isChecked()

class ComboField(QFrame):
    def __init__(self, label : str, items : list = []):
        super().__init__()

        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(4)

        self.label = QLabel(label)
        self.layout.addWidget(self.label)

        self.field = QComboBox()
        for item in items:
            self.field.addItem(item)
        self.layout.addWidget(self.field)
        self.field.setSizePolicy(QSizePolicy.Maximum,
            QSizePolicy.Preferred)

    @property
    def value(self):
        return self.field.currentText()

def el_trunc(s, n=80):
    return s[:min(len(s),n-3)]+'...'

def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')
