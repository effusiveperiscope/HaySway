import os
from collections import deque
from PyQt5.QtWidgets import (QApplication, QComboBox, QMainWindow, QFileDialog,
    QLabel, QFrame, QHBoxLayout, QVBoxLayout, QTabWidget)
from PyQt5.QtGui import (QIntValidator, QDoubleValidator, QKeySequence,
    QDrag)
from archs import (ControllableTalkNetFrame, SoVitsSvc3Frame, SoVitsSvc4Frame
    SoVitsSvc5Frame, RVCFrame)
from recorder import AudioRecorder

# Left side: Tabbed frame for each interface
# Right side: Recorder

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)

        self.vc_tabs = QTabWidget()
        self.vc_tabs.addTab(ControllableTalkNetFrame ,"Controllable TalkNet")
        self.vc_tabs.addTab(SoVitsSvc3Frame,"so-vits-svc 3.0")
        self.vc_tabs.addTab(SoVitsSvc4Frame,"so-vits-svc 4.0")
        self.vc_tabs.addTab(SoVitsSvc5Frame,"so-vits-svc 5.0")
        self.vc_tabs.addTab(RVCFrame,"RVC")
        self.layout.addWidget(self.vc_tabs)

        self.audio_recorder = AudioRecorder()
        self.layout.addWidget(self.audio_recorder)

    def vc_push_fn(self, output_path):
        self.vc_tabs.currentWidget().load_file_ext(output_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    w = MainWindow()
    w.show()
    app.exec()
