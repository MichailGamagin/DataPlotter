from PyQt5.QtWidgets import QComboBox

class MyComboBox(QComboBox):
    """Кастомный выпадающий список"""
    def __init__(self, parent=None):
        super().__init__(parent)

    def wheelEvent(self, event):
        """Обработчик события прокрутки колеса мыши - отключение"""
        event.ignore()
