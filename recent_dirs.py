import os
from collections import deque
from PyQt5.QtCore import (pyqtSignal, QObject)
from PyQt5.QtWidgets import (QApplication, QComboBox, QMainWindow, QFileDialog,
    QFrame, QHBoxLayout, QVBoxLayout)

RECENT_DIR_MAXLEN = 10

class RecentDirComboBox(QComboBox):
    def __init__(self, parent, file_cb):
        super().__init__()
        self.parent = parent
        self.parent.file_updated.connect(self.update_contents)
        self.activated.connect(self.dialog)
        self.file_received_cb = file_cb

    def dialog(self, index):
        self.file_received_cb(
            QFileDialog.getOpenFileNames(self, "Files to process",
            self.recent_dirs[index]))

    def update_contents(self):
        self.clear()
        for d in self.parent.recent_dirs:
            self.addItem(RecentDirs.backtruncate_path(d))

    @property
    def recent_dirs(self):
        return self.parent.recent_dirs

# Shared "recent directories" menu
class RecentDirs(QObject):
    file_updated = pyqtSignal(str)

    def backtruncate_path(path, n=80):
        if len(path) < (n):
            return path
        path = path.replace('\\','/')
        spl = path.split('/')
        pth = spl[-1]
        i = -1

        while len(pth) < (n - 3):
            i -= 1
            if abs(i) > len(spl):
                break
            pth = os.path.join(spl[i],pth)

        spl = pth.split(os.path.sep)
        pth = os.path.join(*spl)
        return '...'+pth

    def create_combo(self, file_cb):
        combo = RecentDirComboBox(self, file_cb)
        return combo

    def __init__(self):
        super().__init__()
        self.recent_dirs = deque(maxlen=RECENT_DIR_MAXLEN)

    def from_list(self, l):
        self.recent_dirs = deque(l, maxlen = RECENT_DIR_MAXLEN)

    def to_list(self):
        return list(self.recent_dirs)

    def cull_duplicates(self):
        self.recent_dirs = deque([d for d in self.recent_dirs if
              os.path.exists(d)], maxlen=RECENT_DIR_MAXLEN)

    def update_with_file(self, file : str):
        dir_path = os.path.abspath(os.path.dirname(file))
        if not dir_path in self.recent_dirs:
            self.recent_dirs.appendleft(dir_path)
        else:
            self.recent_dirs.remove(dir_path)
            self.recent_dirs.appendleft(dir_path)
        self.file_updated.emit(dir_path)
        self.cull_duplicates()
