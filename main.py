import sys
from typing import NoReturn

from PyQt5.QtWidgets import QApplication

from src.gui.views.main_window import MainWindow
from src.utils.logger import Logger
from src import __version__

# Инициализация логгера
Logger()
logger = Logger.get_logger(__name__)

# Коды возврата
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

def main() -> NoReturn:
    """
    Точка входа в приложение.
    Инициализирует главное окно и запускает event loop.
    """
    try:
        logger.info("Запуск приложения")
        app = QApplication(sys.argv)
        window = MainWindow(__version__)
        window.show()
        logger.info("Приложение успешно запущено")
        sys.exit(app.exec_())
    except Exception as e:
        logger.error(f'Ошибка при запуске приложения: {str(e)}', exc_info=True)
        sys.exit(EXIT_FAILURE)


if __name__ == "__main__":
    main()