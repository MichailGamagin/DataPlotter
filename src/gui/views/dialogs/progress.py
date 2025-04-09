import sys
import os



from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtWidgets import (
    QApplication,
    QProgressDialog,
    QProgressBar
)

from src.core.constants import BASE_DIR
from src.gui.styles import STYLE_PROGRESS_BAR
from src.utils.logger import Logger

logger = Logger.get_logger(__name__)

class MyProgressDialog(QProgressDialog):
    """
    Диалоговое окно с индикатором прогресса.

    Attributes:
        bar (QProgressBar): Индикатор прогресса.
    """  

    def __init__(self, title="Загрузка...", label_text="Выполнение...", min_val=0, max_val=100, parent=None):
        super().__init__()
        logger.info("Инициализация MyProgressDialog")
        self.setWindowTitle(title)
        self.setWindowIcon(QtGui.QIcon(os.path.join(BASE_DIR, "icons", "info.png")))
        self.setWindowModality(Qt.WindowModal)
        self.setAutoClose(True)
        self.setAutoReset(True)
        self.setMinimumDuration(0) # чтобы сразу показывался

        self.bar = QProgressBar()
        self.bar.setTextVisible(False)  # Показываем текст прогресса
        self.bar.setFixedSize(620, 30)
        self.bar.setStyleSheet(STYLE_PROGRESS_BAR)
        self.bar.setValue(min_val)
        self.setBar(self.bar)
        self.setFixedSize(650, 100)
        self.setLabelText(label_text)
        logger.info("Инициализация MyProgressDialog успшено заверешена")
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    progress = MyProgressDialog(min_val= 30)
    progress.show()
    progress.exec_()
    app.quit()
    sys.exit(0)
