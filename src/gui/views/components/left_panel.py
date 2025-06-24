from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFormLayout,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from src.gui.styles import COMBO_STYLE_LEFT
from src.utils.logger import Logger
from src.gui.views.components.combo_box import MyComboBox

logger = Logger.get_logger(__name__)


class LeftPanel(QWidget):
    """
    Виджет для отображения левой части интерфейса.

    Attributes:
        combos (list): Список выпадающих списков для выбора параметров.
        data (pd.DataFrame): Данные для отображения в выпадающих списках.
        main_window (QMainWindow): Ссылка на главное окно приложения.
        num_page (QLabel): Метка для отображения номера страницы.
    """

    def __init__(self, data, main_window, parent=None):
        super().__init__(parent)
        logger.info("Инициализация LeftPanel")
        self.combos = []
        self.data = data
        self.main_window = main_window
        self.init_ui()
        logger.info("Инициализация LeftPanel завершена упешно")

    def init_ui(self):
        try:
            logger.debug("Инициализация интерфейса LeftPanel")
            self.main_layout = QVBoxLayout(self)
            self.lbl_layout = QHBoxLayout()

            self.num_page = QLabel()
            self.num_page.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            self.update_label()
            self.lbl_layout.addWidget(self.num_page)
            self.lbl_layout.setContentsMargins(0, 10, 0, 25)
            self.main_layout.addLayout(self.lbl_layout)
            for i in range(15):
                form = QFormLayout()
                form.setHorizontalSpacing(15)
                form.setVerticalSpacing(20)
                self.main_layout.addLayout(form)
                combo = MyComboBox()
                lbl = QLabel(f"Линия №{i+1}")
                lbl.setStyleSheet(
                    "QLabel {\n"
                    "font-size: 14px; \n"
                    "font-weight: 500;\n"
                    "color: black;\n"
                    "min-width: 90px;\n"
                    "}\n"
                )
                combo.addItems(self.data.columns[1:])
                combo.setCurrentIndex(-1)
                combo.currentIndexChanged.connect(
                    lambda _, idx=i: self.main_window.plot_selection(idx)
                )
                combo.setStyleSheet(COMBO_STYLE_LEFT)
                combo.cleared.connect(
                    lambda idx=i: self.main_window.plot_selection(idx)
                )
                self.combos.append(combo)
                form.addRow(lbl, combo)
            logger.info("Интерфейс LeftPanel успешно инициализирован")
        except Exception as e:
            logger.error(f"Ошибка при настройке пользовательского интерфейса LeftPanel: {str(e)}", exc_info=True)

    def update_label(self):
        """Метод обновления номера графика"""
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.num_page.setFont(font)
        self.num_page.setText(
            f"График №{self.main_window.current_page + 1} из {len(self.main_window.pages)}"
        )
