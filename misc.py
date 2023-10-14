from PyQt5.QtWidgets import (QFrame, QLineEdit, QLabel, QHBoxLayout, QCheckBox,
    QComboBox)

class NumField(QFrame):
    def __init__(self, label : str, default : str, validator):
        super().__init__()

        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)

        self.label = QLabel(label)
        self.layout.addWidget(self.label)

        self.field = QLineEdit(default)
        self.field.setValidator(validator)
        self.layout.addWidget(self.field)

    @property
    def value(self):
        return self.field.text()

class BoolField(QFrame):
    def __init__(self, label : str, default : bool = False):
        super().__init__()

        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)

        self.label = QLabel(label)
        self.layout.addWidget(self.label)

        self.field = QCheckBox(default)
        self.layout.addWidget(self.field)

    @property
    def value(self):
        return self.field.isChecked()

class ComboField(QFrame):
    def __init__(self, label : str, items : list = []):
        super().__init__()

        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)

        self.label = QLabel(label)
        self.layout.addWidget(self.label)

        self.field = QComboBox(default)
        for item in items:
            self.field.addItem(item)
        self.layout.addWidget(self.field)

    @property
    def value(self):
        return self.field.currentText()

def el_trunc(s, n=80):
    return s[:min(len(s),n-3)]+'...'
