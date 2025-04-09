import sys
import os

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from src.core.constants import ICONS_DIR
from src.gui.views.dialogs.message import MessageWindow
from src.gui.views.word.alternative_lines import AlternativeLines
from src.utils.logger import Logger

logger = Logger.get_logger(__name__)


class WordSettings(QWidget):
    """
    Виджет для отображения интерфейса настроки параметров Word документа.

    Attributes:
        надо дописать документацию 
    """
    params = {
        "font": None,
        "font-size": None,
        "int-before": None,
        "int-after": None,
        "line-spacing": None,
        "pic-height": None,
        "pic-width": None,
        "pict": None,
        "num-section": None,
        "first-pic": None,
        "mode-name": None,
    }
    def __init__(self, parent = None):
        super().__init__()
        logger.info('Инициализация WordSettings')
        self.parent = parent
        self.params = self.parent.params
        self.setWindowTitle('Настройка Word')

        self.widget = QtWidgets.QWidget()
        self.widget.setGeometry(QtCore.QRect(21, 13, 520, 312))
        self.central_layout = QtWidgets.QVBoxLayout(self.widget)
        self.central_layout.setContentsMargins(10, 10, 10, 10)
        self.central_layout.setSpacing(3)

        # Шрифт
        self.font_layout = QtWidgets.QHBoxLayout()
        self.font_combo = QtWidgets.QFontComboBox(self.widget)
        self.font_layout.addWidget(self.font_combo)
        self.font_height_combo = QtWidgets.QComboBox(self.widget)
        self.font_layout.addWidget(self.font_height_combo)
        spacerItem = QtWidgets.QSpacerItem(
            150, 16, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.font_layout.addItem(spacerItem)
        self.btn_layout = QtWidgets.QVBoxLayout()
        self.btn_layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.accept_btn = QtWidgets.QPushButton(self.widget)
        self.accept_btn.clicked.connect(self.accept)
        self.btn_layout.addWidget(self.accept_btn)
        self.cancel_btn = QtWidgets.QPushButton(self.widget)
        self.cancel_btn.clicked.connect(self.cancel)
        self.btn_layout.addWidget(self.cancel_btn)
        self.alternative_lines_btn = QtWidgets.QPushButton(self.widget)
        self.alternative_lines_btn.clicked.connect(self.open_alt_lines)
        self.btn_layout.addWidget(self.alternative_lines_btn)
        self.font_layout.addLayout(self.btn_layout)
        self.central_layout.addLayout(self.font_layout)

        # Интервал и размер рисунка
        self.horizontalLayout = QtWidgets.QHBoxLayout()

        # Интервал
        self.interval_groupBox = QtWidgets.QGroupBox(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.interval_groupBox.sizePolicy().hasHeightForWidth()
        )
        self.interval_groupBox.setSizePolicy(sizePolicy)
        self.interval_groupBox.setMinimumSize(QtCore.QSize(270, 80))
        self.interval_groupBox.setMaximumSize(QtCore.QSize(330, 80))
        self.widget1 = QtWidgets.QWidget(self.interval_groupBox)
        self.widget1.setGeometry(QtCore.QRect(20, 20, 100, 52))
        self.before_after_layout = QtWidgets.QVBoxLayout(self.widget1)
        self.before_after_layout.setContentsMargins(0, 0, 0, 0)
        self.before_layout = QtWidgets.QHBoxLayout()
        self.before_lbl = QtWidgets.QLabel(self.widget1)
        self.before_layout.addWidget(self.before_lbl)
        self.before_spinBox = QtWidgets.QSpinBox(self.widget1)
        self.before_layout.addWidget(self.before_spinBox)
        self.before_after_layout.addLayout(self.before_layout)
        self.after_layout = QtWidgets.QHBoxLayout()
        self.after_lbl = QtWidgets.QLabel(self.widget1)
        self.after_layout.addWidget(self.after_lbl)
        self.after_spintBox = QtWidgets.QSpinBox(self.widget1)
        self.after_layout.addWidget(self.after_spintBox)
        self.before_after_layout.addLayout(self.after_layout)
        self.widget2 = QtWidgets.QWidget(self.interval_groupBox)
        self.widget2.setGeometry(QtCore.QRect(160, 20, 100, 55))
        self.line_spacing_layout = QtWidgets.QVBoxLayout(self.widget2)
        self.line_spacing_layout.setContentsMargins(0, 0, 0, 0)
        self.line_spacing_layout.setSpacing(15)
        self.line_spacing_lbl = QtWidgets.QLabel(self.widget2)
        self.line_spacing_layout.addWidget(self.line_spacing_lbl)
        self.line_spacing_combo = QtWidgets.QComboBox(self.widget2)
        self.line_spacing_combo.addItem("Одинарный")
        self.line_spacing_combo.addItem("1,5 строки")
        self.line_spacing_layout.addWidget(self.line_spacing_combo)
        self.horizontalLayout.addWidget(self.interval_groupBox)
        # Пустое место
        self.horizontalSpacer_3 = QSpacerItem(
            45, 20, QSizePolicy.Fixed, QSizePolicy.Minimum
        )

        self.horizontalLayout.addItem(self.horizontalSpacer_3)
        # Размер рисунка
        self.pic_size = QtWidgets.QGroupBox(self.widget)
        self.pic_size.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pic_size.sizePolicy().hasHeightForWidth())
        self.pic_size.setSizePolicy(sizePolicy1)
        self.pic_size.setMinimumSize(QtCore.QSize(100, 80))
        self.pic_size.setMaximumSize(QtCore.QSize(300, 80))
        self.widget3 = QWidget(self.pic_size)
        self.widget3.setGeometry(QtCore.QRect(11, 20, 151, 48))
        self.formLayout = QtWidgets.QFormLayout(self.widget3)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.pic_width_lbl = QtWidgets.QLabel(self.widget3)

        self.formLayout.setWidget(
            0, QtWidgets.QFormLayout.LabelRole, self.pic_width_lbl
        )

        self.pic_width_doubleSpinBox = QtWidgets.QDoubleSpinBox(self.widget3)
        self.formLayout.setWidget(
            0, QtWidgets.QFormLayout.FieldRole, self.pic_width_doubleSpinBox
        )

        self.pic_height_lbl = QtWidgets.QLabel(self.widget3)

        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.LabelRole, self.pic_height_lbl
        )

        self.pic_height_doubleSpinBox = QtWidgets.QDoubleSpinBox(self.widget3)

        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.FieldRole, self.pic_height_doubleSpinBox
        )
        self.horizontalLayout.addWidget(self.pic_size)

        self.central_layout.addLayout(self.horizontalLayout)

        # Подпись
        self.cuption_groupBox = QtWidgets.QGroupBox(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.cuption_groupBox.sizePolicy().hasHeightForWidth()
        )
        self.cuption_groupBox.setSizePolicy(sizePolicy)
        self.cuption_groupBox.setMinimumSize(QtCore.QSize(500, 150))
        self.cuption_groupBox.setMaximumSize(QtCore.QSize(700, 150))
        self.widget3 = QtWidgets.QWidget(self.cuption_groupBox)
        self.widget3.setGeometry(QtCore.QRect(20, 50, 461, 73))
        self.first_part = QtWidgets.QHBoxLayout(self.widget3)
        self.first_part.setContentsMargins(0, 0, 0, 0)
        self.mode_name_lbl = QtWidgets.QLabel(self.widget3)
        self.first_part.addWidget(self.mode_name_lbl)
        self.mode_name_textEdit = QtWidgets.QTextEdit(self.widget3)
        self.first_part.addWidget(self.mode_name_textEdit)
        self.widget4 = QtWidgets.QWidget(self.cuption_groupBox)
        self.widget4.setGeometry(QtCore.QRect(20, 20, 461, 22))
        self.second_part = QtWidgets.QHBoxLayout(self.widget4)
        self.second_part.setContentsMargins(0, 0, 0, 0)
        self.picture_line_edit = QtWidgets.QLineEdit(self.widget4)
        self.second_part.addWidget(self.picture_line_edit)
        self.num_section_lbl = QtWidgets.QLabel(self.widget4)
        self.second_part.addWidget(self.num_section_lbl)
        self.num_section_lineEdit = QtWidgets.QLineEdit(self.widget4)
        self.second_part.addWidget(self.num_section_lineEdit)
        self.num_first_pic_lbl = QtWidgets.QLabel(self.widget4)
        self.second_part.addWidget(self.num_first_pic_lbl)
        self.num_first_pic_spinBox = QtWidgets.QSpinBox(self.widget4)
        self.num_first_pic_spinBox.setProperty("value", 1)
        self.second_part.addWidget(self.num_first_pic_spinBox)
        self.central_layout.addWidget(self.cuption_groupBox)

        self.setLayout(self.central_layout)
        self.setWindowIcon(QIcon(os.path.join(ICONS_DIR, "icons", "settings.jpg")))
        self.retranslateUi()
        logger.info('Инициализация WordSettings успешно завершена')

    def retranslateUi(self):
        self.font_height_combo.addItems(
            ["8", "9", "10", "11", "12", "14", "16", "18", "20", "22"]
        )
        self.accept_btn.setText("Применить")
        self.cancel_btn.setText("Отмена")
        self.alternative_lines_btn.setText('Настройка подписей\nрисунков')
        self.interval_groupBox.setTitle("Интервал")
        self.before_lbl.setText("Перед:")
        self.after_lbl.setText("После:")
        self.line_spacing_lbl.setText("Междустрочный:")
        self.pic_size.setTitle("Рисунок")
        self.pic_width_lbl.setText('Ширина, См:')
        self.pic_height_lbl.setText('Высота, См:')
        self.mode_name_textEdit.setPlaceholderText(
                "Потеря нормального расхода питательной воды (отключение всех насосов питательной воды)",
        )
        self.num_section_lbl.setText("Номер раздела:")
        self.num_section_lineEdit.setPlaceholderText("5.1")
        self.num_first_pic_lbl.setText("Номер первого рисунка:")
        self.cuption_groupBox.setTitle("Подпись")
        self.mode_name_lbl.setText("Наименование режима:")

        if all(value is None for value in self.params.values()):
            self.set_default_settings()
        else:
            self.set_usr_settings()

    def set_default_settings(self):
        
        self.font_combo.setCurrentText("Times New Roman")
        self.font_height_combo.setCurrentIndex(0)
        self.line_spacing_combo.setCurrentIndex(0)
        self.after_spintBox.setValue(0)
        self.before_spinBox.setValue(0)
        self.pic_width_doubleSpinBox.setValue(16.0)
        self.pic_height_doubleSpinBox.setValue(9.5)
        self.picture_line_edit.setText("Рисунок") 
        self.num_first_pic_spinBox.setValue(1)

    def set_usr_settings(self):
        logger.info('Настройка пользовательских параметров Word из файла конфигурации')
        self.font_combo.setCurrentText(self.params['font'])
        self.font_height_combo.setCurrentText(self.params["font-size"])
        self.line_spacing_combo.setCurrentText(self.params["line-spacing"])
        self.before_spinBox.setValue(self.params["int-before"])
        self.after_spintBox.setValue(self.params['int-after'])
        self.pic_width_doubleSpinBox.setValue(self.params["pic-width"])
        self.pic_height_doubleSpinBox.setValue(self.params["pic-height"])
        self.picture_line_edit.setText(self.params["pict"])
        self.num_section_lineEdit.setText(self.params["num-section"])
        self.num_first_pic_spinBox.setValue(self.params["first-pic"])
        self.mode_name_textEdit.setPlainText(self.params["mode-name"])
        logger.info('Настройка пользовательских параметров Word из файла конфигурации успешно завершена')

    def accept(self):
        logger.info('Нажата кнопка Применить')
        try:
            self.params['font'] = self.font_combo.currentText()
            self.params["font-size"] = self.font_height_combo.currentText()
            self.params["line-spacing"] = self.line_spacing_combo.currentText()
            self.params["int-after"] = self.after_spintBox.value()
            self.params["int-before"] = self.before_spinBox.value()
            self.params["pic-width"] = self.pic_width_doubleSpinBox.value()
            self.params["pic-height"] = self.pic_height_doubleSpinBox.value()
            self.params["pict"] = self.picture_line_edit.text().strip()
            self.params["num-section"] = self.num_section_lineEdit.text().strip()
            self.params["first-pic"] = self.num_first_pic_spinBox.value()
            self.params["mode-name"] = self.mode_name_textEdit.toPlainText()

            self.font_combo.setCurrentText(self.font_combo.currentText())
            self.font_height_combo.setCurrentText(self.font_height_combo.currentText())
            self.line_spacing_combo.setCurrentText(
                self.line_spacing_combo.currentText()
            )
            self.after_spintBox.setValue(self.after_spintBox.value())
            self.before_spinBox.setValue(self.before_spinBox.value())
            self.pic_width_doubleSpinBox.setValue(self.pic_width_doubleSpinBox.value())
            self.pic_height_doubleSpinBox.setValue(
                self.pic_height_doubleSpinBox.value()
            )
            self.picture_line_edit.setText(self.picture_line_edit.text().strip())
            self.num_section_lineEdit.setText(self.num_section_lineEdit.text().strip())
            self.num_first_pic_spinBox.setValue(self.num_first_pic_spinBox.value())
            self.mode_name_textEdit.setPlainText(self.mode_name_textEdit.toPlainText()) 

            self.parent.params = self.params
            logger.info(f"Шрифт: {self.font_combo.currentText()}")
            logger.info(f"Высота шрифта: {self.font_height_combo.currentText()}")
            logger.info(f"Перед: {self.before_spinBox.value()}")
            logger.info(f"После: {self.after_spintBox.value()}")
            logger.info(f"Междустрочный: {self.line_spacing_combo.currentText()}")
            logger.info(f"Ширина рисунка: {self.pic_width_doubleSpinBox.value()}")
            logger.info(f"Высота рисунка: {self.pic_height_doubleSpinBox.value()}")
            logger.info(f"Рисунок/Picture: {self.picture_line_edit.text().strip()}")
            logger.info(f"Номер раздела: {self.num_section_lineEdit.text().strip()}")
            logger.info(f"Номер первого рисунка: {self.num_first_pic_spinBox.value()}")
            logger.info(f"Наименование режима: {self.mode_name_textEdit.toPlainText()}")

        except Exception as e:
            msg = MessageWindow(
                    "Ошибка применения",
                    f"Текст ошибки:\n{str(e)}",
                )
            logger.error(f"Ошибка в логике применения: {str(e)}", exc_info=True)
            msg.exec_()

    def cancel(self):
        self.close()

    def open_alt_lines(self):
        self.alt_lines = AlternativeLines(main_window=self.parent)
        self.alt_lines.setWindowModality(Qt.ApplicationModal)
        self.alt_lines.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WordSettings()
    window.show()
    sys.exit(app.exec_())
