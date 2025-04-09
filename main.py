
import sys

from  PyQt5.QtWidgets import QApplication

from src.gui.views.main_window import MainWindow
from src.utils.logger import Logger


Logger()
logger = Logger.get_logger(__name__)

def main():
    try:
        logger.info("Запуск приложения")
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        logger.info("Приложение успешно запущено")
        sys.exit(app.exec_())
    except Exception as e:
        logger.error(f'Ошибка при запуске приложения: {str(e)}', exc_info=True)


if __name__ == "__main__":
    main()