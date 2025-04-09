from PyQt5.QtWidgets import QLineEdit


class MyLineEdit(QLineEdit):
    """
    Поле ввода текста с поддержкой перетаскивания файлов.

    Attributes:
        None
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            self.setText(file_path)
