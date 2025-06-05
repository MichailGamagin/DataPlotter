import sys
import os

from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets

from src.gui.styles import WORK_SPACE_STYLE, ALTERNATIVE_LINES_STACK_STYLE
from src.core.constants import ICONS_DIR
from src.utils.logger import Logger

logger = Logger.get_logger(__name__)

class AlternativeLines(QtWidgets.QWidget):
    """
    Виджет для отображения интерфейса альтернативных подписей линий
    """
    def __init__(self, parent = None, main_window = None):
        super().__init__()
        logger.info("Инициализация AlternativeLines")
        self.parent = parent
        self.main_window = main_window
        self.setWindowTitle("Настройка альтернативных подписей линий")
        self.setFixedSize(1180, 800)  
        self.setWindowIcon(QtGui.QIcon(os.path.join(ICONS_DIR, "icons", "settings.jpg")))
        self.pages = self.main_window.pages
        self.textEdits = {}
        self.headers = []
        self.cuptions = {}
        self.graph_ids = {}  # Словарь для хранения ID графиков
        self.init_ui()
        logger.info(f"Инициализация AlternativeLines успешно завершена")

    def init_ui(self):
        # Основной макет
        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # --- Рабочая область (QTreeWidget) ---
        self.work_space = QtWidgets.QTreeWidget()
        self.work_space.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.work_space.setMinimumWidth(221)
        self.work_space.setStyleSheet(WORK_SPACE_STYLE)
        self.work_space.setHeaderHidden(False)
        self.work_space.headerItem().setText(0, "Рабочая область")
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.work_space.headerItem().setFont(0, font) 
        self.work_space.headerItem().setTextAlignment(0, QtCore.Qt.AlignCenter)
        self.work_space.itemClicked.connect(self.on_graph_clicked)

        # Заполняем QTreeWidget
        root = QtWidgets.QTreeWidgetItem(self.work_space)
        root.setText(0, "Графики")
        for graph_num in range(len(self.pages)):
            item = QtWidgets.QTreeWidgetItem(root)
            final_name = f"График №{graph_num + 1}"
            item.setText(0, final_name)

        main_layout.addWidget(self.work_space)

        # --- Stacked Widget ---
        self.stack = QtWidgets.QStackedWidget()
        self.stack.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.stack.setMinimumWidth(930)
        self.stack.setStyleSheet(ALTERNATIVE_LINES_STACK_STYLE)

        # Динамически создаем страницы
        self.create_pages()
        self.set_text_to_textEdit()
        main_layout.addWidget(self.stack)

    def create_pages(self):
        """Создание страниц"""
        for graph_num in range(0, len(self.pages)):
            graph_id = self.pages[graph_num].get('id', f'graph_{graph_num}')  # Получаем или генерируем ID
            self.graph_ids[graph_num] = graph_id
            self.add_page(graph_num)

    def add_page(self, graph_num: int):
        """Метод добавления страницы"""
        page_indx = graph_num
        page = QtWidgets.QWidget()

        # Количество полей ввода в главном окне левой панели на соответствующей странице
        count_field = len(self.pages[page_indx]["left"].combos)

        page_layout = QtWidgets.QVBoxLayout(page)
        page_layout.setContentsMargins(10, 10, 10, 10)
        page_layout.setSpacing(10)

        # Номер графика
        num_graphs_layout = QtWidgets.QHBoxLayout()
        num_graph_lbl = QtWidgets.QLabel(f'График №{graph_num+1}')
        num_graph_lbl.setFont(QtGui.QFont("Yu Gothic UI", 18))

        self.headers.append(num_graph_lbl.text())

        num_graphs_layout.addWidget(num_graph_lbl)
        num_graphs_layout.addStretch(1)
        page_layout.addLayout(num_graphs_layout)

        # "Действующее название" и "Альтернативное название"
        caption_layout = QtWidgets.QHBoxLayout()
        caption_layout.setSpacing(15)
        caption_layout.addSpacing(85)
        font = QtGui.QFont("Yu Gothic UI", 12, QtGui.QFont.Bold)
        current_name_lbl = QtWidgets.QLabel("Действующее название")
        current_name_lbl.setToolTip('Наименование линий под номером раздела,\n'
                                    'которое будет установлено, если\n'
                                    'не задано альтернативной подписи')
        current_name_lbl.setFont(font)
        current_name_lbl.setAlignment(QtCore.Qt.AlignCenter)
        caption_layout.addWidget(current_name_lbl)
        alternative_name_lbl = QtWidgets.QLabel("Альтернативное название")
        alternative_name_lbl.setToolTip('Наименование линий под номером раздела,\n'
                                        'которое будет установлено, вместо\n'
                                        'действующих линий')
        alternative_name_lbl.setFont(font)
        alternative_name_lbl.setAlignment(QtCore.Qt.AlignCenter)
        caption_layout.addWidget(alternative_name_lbl)
        page_layout.addLayout(caption_layout)

        # Линии и метки
        lines_and_text_layout = QtWidgets.QHBoxLayout()
        lines_and_text_layout.setContentsMargins(5, 5, 5, 5)
        form_layout = QtWidgets.QFormLayout()
        form_layout.setContentsMargins(5, 5, 5, 5)

        for i in range(count_field):
            lbl = QtWidgets.QLabel(f"Линия {i + 1}")
            lbl.setFont(QtGui.QFont("Yu Gothic UI", 10))
            line_edit = QtWidgets.QLineEdit()
            line_edit.setReadOnly(True)
            form_layout.addRow(lbl, line_edit)
            # Получаем текс из комбобоксов левой панели главного окна соответствующей страницы
            text = self.pages[page_indx]["left"].combos[i].currentText()
            line_edit.setText(text)
        lines_and_text_layout.addLayout(form_layout)

        textEdit = QtWidgets.QTextEdit()
        textEdit.setMinimumWidth(394)
        textEdit.setMaximumWidth(426)
        self.textEdits[f"{page_indx}"] = textEdit
        lines_and_text_layout.addWidget(textEdit)

        page_layout.addLayout(lines_and_text_layout)

        # Кнопки
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch(1)
        save_btn = QtWidgets.QPushButton("Сохранить")
        save_btn.clicked.connect(self.save)
        button_layout.addWidget(save_btn)
        page_layout.addLayout(button_layout)

        self.stack.addWidget(page)

    def on_graph_clicked(self, item, column=0):
        """Обработчик события клика на элемент в QTreeWidget"""
        graph_name = item.text(0)
        if graph_name != "Графики":
            try:
                graph_number = int(graph_name.split('№')[1])
                self.stack.setCurrentIndex(graph_number - 1)
            except (IndexError, ValueError):
                logger.debug(f"Ошибка обработки имени графика: {graph_name}")

    def accept_changes(self, num_graph: int = None):
        """
        Сохраняет изменения для текущей страницы.
        """
        if num_graph is None:
            num_graph = self.stack.currentIndex()
        textEdit = self.textEdits[f"{num_graph}"]
        text = textEdit.toPlainText().strip()
        graph_id = self.graph_ids[num_graph]
        self.cuptions[graph_id] = text

    def set_text_to_textEdit(self):
        """Метод установки текста в textEdit с использованием ID графиков"""
        for i, graph_id in self.graph_ids.items():
            if graph_id in self.main_window.alternative_captions:
                text = self.main_window.alternative_captions[graph_id]
                self.textEdits[f"{i}"].setText(text)
                self.cuptions[graph_id] = text

    def update_alternative_captions(self):
        """Обновляет словарь альтернативных подписей при изменении графиков"""
        new_captions = {}
        for i, graph_id in self.graph_ids.items():
            if graph_id in self.cuptions:
                new_captions[graph_id] = self.cuptions[graph_id]
        self.cuptions = new_captions

    def save(self):
        """
        Сохранение всех изменений в главное окно по ID графиков
        """
        for idx in self.graph_ids.keys():
            self.accept_changes(idx)
        self.main_window.alternative_captions.update(self.cuptions)
        QMessageBox.information(
            self, "Успешно", "Все изменения сохранены."
        )


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AlternativeLines()
    window.show()
    sys.exit(app.exec_())
