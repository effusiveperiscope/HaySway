from PyQt5.QtCore import (QSize)
from PyQt5.QtWidgets import (QFrame, QLineEdit, QLabel, QHBoxLayout, QCheckBox,
    QComboBox, QSizePolicy)

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
