import sys
from PyQt5.QtWidgets import QMessageBox, QApplication
from src.utils.logger import Logger

logger = Logger.get_logger(__name__)

class MessageWindow(QMessageBox):
    """
    Диалоговое окно для отображения сообщений об ошибках.

    Attributes:
        text (str): Текст сообщения.
        detText (str): Детальный текст ошибки (необязательный).
    """
    def __init__(self, text: str, detText: str = None):
        logger.info(f'Инициализация MessageWindow')
        super().__init__()
        self.setIcon(self.Critical)
        self.setWindowTitle("Ошибка")
        self.text = text
        self.setText(self.text)
        if detText is not None:
            self.detText = detText
            self.setDetailedText(f"Текст ошибки: {self.detText}")
        logger.info(f'Инициализация MessageWindow успешно завершена')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    msg = MessageWindow("Ошибка загрузки состояния", "File not found")
    msg.exec_()
    print(msg.text, msg.detText)
    sys.exit(app.exec_())
    # msg.exec_()
