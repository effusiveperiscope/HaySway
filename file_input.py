from recent_dirs import *
from PyQt5.QtWidgets import (QApplication, QComboBox, QMainWindow, QFileDialog,
    QLabel, QFrame, QHBoxLayout, QVBoxLayout, QPushButton)
from preview import AudioPreviewWidget

recent_dirs = RecentDirs()

class FileButton(QPushButton):
    fileDropped = pyqtSignal(list)
    def __init__(self, label = "Files to Convert"):
        super().__init__(label)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            files = []
            for url in event.mimeData().urls():
                if not url.toLocalFile():
                    continue
                files.append(url.toLocalFile())
            self.fileDropped.emit(files)
            event.acceptProposedAction()
        else:
            event.ignore()
        pass

class AudioFilesInput(QFrame):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(4)

        self.files = []

        self.file_button = FileButton()
        self.file_button.fileDropped.connect(self.file_cb)
        self.layout.addWidget(self.file_button)

        self.file_label = QLabel("Files: "+str(self.files))
        self.file_label.setWordWrap(True)
        self.layout.addWidget(self.file_label)

        self.layout.addWidget(QLabel("Recent directories:"))
        self.recent_dirs_box = recent_dirs.create_combo(self.file_cb)
        self.layout.addWidget(self.recent_dirs_box)

        self.preview = AudioPreviewWidget()
        self.layout.addWidget(self.preview)

    def file_cb(self, files : list):
        self.files = files
        self.file_label.setText("Files: "+str(files))
        if len(files) > 0:
            self.preview.setText("Preview - "+str(files[0]))
            self.preview.from_file(files[0])

    def load_files(self, files : list):
        self.file_cb(files)
