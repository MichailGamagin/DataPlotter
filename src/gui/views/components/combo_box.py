from PyQt5.QtWidgets import QComboBox, QCompleter
from PyQt5.QtCore import QStringListModel, Qt

# model = QStringListModel
class MyComboBox(QComboBox):
    """Кастомный выпадающий список"""
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
        # self.lineEdit().textEdited.connect(self.update_completer)
        self._original_items = []

    def wheelEvent(self, event):
        """Обработчик события прокрутки колеса мыши - отключение"""
        event.ignore()

    def addItems(self, list: list):
        super().addItems(list)
        self._original_items.extend(list)
        self._update_model()

    def _update_model(self):
        self.model.setStringList(self._original_items)

    # def update_completer(self, text):
    #     self.completer.setCompletionPrefix(text)
    #     if text:
    #         self.showPopup()
    #     else: 
    #         self.hidePopup()
