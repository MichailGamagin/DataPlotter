from PyQt5.QtWidgets import QComboBox

class MyComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)

    def wheelEvent(self, event):
        event.ignore()
