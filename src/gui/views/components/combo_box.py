from PyQt5.QtWidgets import QComboBox, QCompleter
from PyQt5.QtCore import QStringListModel, Qt, pyqtSignal

class MyComboBox(QComboBox):
    """Кастомный выпадающий список"""
    cleared = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEditable(True)
        self.setPlaceholderText("Параметр, кг")
        self.setMaxVisibleItems(30)
        self.model = QStringListModel()
        self.completer = QCompleter()
        self.completer.setModel(self.model)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.setFilterMode(Qt.MatchContains)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setMaxVisibleItems(30)
        self.setCompleter(self.completer)
        self._original_items = []
        self.currentTextChanged.connect(self._on_text_changed)

    def wheelEvent(self, event):
        """Обработчик события прокрутки колеса мыши - отключение"""
        event.ignore()

    def addItems(self, list: list):
        super().addItems(list)
        self._original_items.extend(list)
        self._update_model()

    def insertItems(self, index: int, list: list):
        super().insertItems(index, list)
        self._original_items.extend(list)
        self._update_model()

    def _update_model(self):
        self.model.setStringList(self._original_items)

    def _on_text_changed(self, text):
        if not text:
            self.cleared.emit()

    def enterEvent(self, event):
        super().enterEvent(event)
        self.setToolTip(self.currentText())

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.setToolTip("")