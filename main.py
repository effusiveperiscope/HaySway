import os
from collections import deque
from PyQt5.QtWidgets import (QApplication, QComboBox, QMainWindow, QFileDialog,
    QLabel, QFrame, QHBoxLayout, QVBoxLayout, QTabWidget, QWidget)
from PyQt5.QtGui import (QIntValidator, QDoubleValidator, QKeySequence,
    QDrag)
from archs import (ControllableTalkNetFrame, SoVitsSvc3Frame, SoVitsSvc4Frame,
    SoVitsSvc5Frame, RVCFrame)
from recorder import AudioRecorder
import sys
import traceback

class CentralWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout(self)

        self.vc_tabs = QTabWidget()
        self.vc_tabs.addTab(ControllableTalkNetFrame(),"Controllable TalkNet")
        self.vc_tabs.addTab(SoVitsSvc3Frame(),"so-vits-svc 3.0")
        self.vc_tabs.addTab(SoVitsSvc4Frame(),"so-vits-svc 4.0")
        self.vc_tabs.addTab(SoVitsSvc5Frame(),"so-vits-svc 5.0")
        self.vc_tabs.addTab(RVCFrame(),"RVC")
        self.layout.addWidget(self.vc_tabs)

        self.audio_recorder = AudioRecorder(self.vc_push_fn)
        self.layout.addWidget(self.audio_recorder)

    def vc_push_fn(self, output_path):
        self.vc_tabs.currentWidget().load_file_ext(output_path)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.central_widget = CentralWidget()
        #self.setCentralWidget(self) # Did you know this causes a hang?
        self.setCentralWidget(self.central_widget)
        self.setWindowTitle('Hay Sway')

def interrupt_handler(signal, frame):
    print("Keyboard interrupt received. Printing stack trace:")
    traceback.print_stack(frame)
    sys.exit(1)  # Exit the script with a non-zero status

def test():
    import requests
    payload = {
        'architecture': 'controllable_talknet',
        'Inputs': {
            'User Text': 'butt',
            'User Audio': ''
        },
        'Options': {
            'Architecture': 'controllable_talknet',
            'Character': 'Twilight Sparkle',
            'Disable Reference Audio': True,
            'Pitch Factor': 0,
            'Auto Tune': False,
            'Reduce Metallic Sound': False},
        'Output File': "a.wav"
    }

    response = requests.post('http://127.0.0.1:7802'+'/generate',
        headers={'Content-Type': 'application/json'}, json=payload)
    code = response.status_code
    if code != 200:
        raise Exception("Docker bridge returned non-200 error code "+
            str(code))

if __name__ == "__main__":
    #test()
    app = QApplication(sys.argv)

    w = MainWindow()
    w.show()
    app.exec()
