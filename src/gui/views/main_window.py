#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Файл основного окна приложения
"""
import sys
import os
import yaml

from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QStackedWidget,
    QToolBar,
    QLabel,
    QMessageBox,
    QSizePolicy,
    QShortcut,
    QStatusBar,
    QAction,
    QDesktopWidget,
)
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtCore import Qt

from src.gui.styles import MY_LINE_EDIT_STYLE, STACK_WIDGET_STYLE
from src.core.constants import (
    BASE_DIR,
    ENCODING,
    DEFAULT_FILE_PATH,
    SAVE_FILE,
    DEFAULT_DIR,
    ICONS_DIR,
)

from src.core.data_loader import load_data_from
from src.gui.views.components.lyne_edit import MyLineEdit
from src.gui.views.components.left_panel import LeftPanel
from src.gui.views.components.plot_area import PlotArea
from src.gui.views.dialogs.message import MessageWindow
from src.gui.views.dialogs.progress import MyProgressDialog
from src.gui.views.word.settings import WordSettings
from src.gui.views.word.word_export import Word
from src.utils.logger import Logger

logger = Logger.get_logger(__name__)


class MainWindow(QMainWindow):
    """
    Главное окно приложения для построения графиков.

    Attributes:
        pages (list): Список словарей, содержащих информацию о каждой странице (графике).
        current_page (int): Индекс текущей активной страницы.
        data_file_path (str): Путь к файлу с данными.
        data (pd.DataFrame): DataFrame с данными для построения графиков.
        stack (QStackedWidget): Виджет для отображения страниц.
        alternative_captions(dict): словарь для альтернативных названий линий
        params(dict): словарь для хранения настроек Word для документа(шрифт, интервал и тд)
    """

    def __init__(self, version: str):
        super().__init__()
        logger.info("Инициализация MainWindow")
        self.pages = []
        self.params = {}
        self.alternative_captions = {}
        self.version = version
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        self.setStyleSheet(STACK_WIDGET_STYLE)
        self.current_page = 0
        self.data_file_path = DEFAULT_FILE_PATH
        self.data = load_data_from(self.data_file_path, ENCODING)
        self.init_ui()
        reply = QMessageBox.question(
            self,
            "Загрузить последний файл состояния?",
            f"Загрузить последний файл состояния?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes,
        )
        logger.info("Интерфейс MainWindow успешно инициализирован")
        if reply != QMessageBox.No:
            self._load_state()

    def init_ui(self):
        logger.info(f"Инициализация пользовательского интерфейса MainWindow")
        self.init_menu()
        self.init_toolbar()

        self.shortcut_right = QShortcut(QKeySequence("Right"), self)
        self.shortcut_right.activated.connect(self.next_page)
        self.shortcut_left = QShortcut(QKeySequence("Left"), self)
        self.shortcut_left.activated.connect(self.prev_page)

        if self.data_file_path == "":
            self.add_page()
        self.update_buttons()

        # Window settings
        self.setWindowTitle(f"Data Plotter v{self.version}")
        self.setWindowIcon(QIcon(os.path.join(ICONS_DIR, "icons", "main_icon.png")))

        self.word_settings = WordSettings(parent=self).accept()
        logger.info("Пользовательский интерфейс MainWindow успешно инициализирован")

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.show()
        self.path_ent.clearFocus()
        self.setFocus()

    def init_menu(self):
        """Инициализация меню"""
        self.menubar = self.menuBar()
        file_menu = self.menubar.addMenu("Файл")
        file_menu.addAction(
            QIcon(os.path.join(ICONS_DIR, "icons", "new_project.jpg")),
            "Новый проект",
            self.new_project,
        )

    def init_toolbar(self):
        """Инициализация ToolBar'a"""
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        # Navigation buttons
        self.insert_page_left_act = QAction(
            QIcon(os.path.join(ICONS_DIR, "icons", "insert_left.png")),
            "Вставить график слева",
            self,
        )
        self.insert_page_left_act.setToolTip("Вставить график слева")
        self.insert_page_left_act.triggered.connect(self.insert_page_left)

        self.add_page_act = QAction(
            QIcon(os.path.join(ICONS_DIR, "icons", "add_graph.png")),
            "Добавить график",
            self,
        )
        self.add_page_act.setToolTip("Добавить график (в конец)")
        self.add_page_act.triggered.connect(self.add_page)

        self.insert_page_right_act = QAction(
            QIcon(os.path.join(ICONS_DIR, "icons", "insert_right.png")),
            "Вставить график справа",
            self,
        )
        self.insert_page_right_act.setToolTip("Вставить график справа")
        self.insert_page_right_act.triggered.connect(self.insert_page_right)

        self.remove_page_act = QAction(
            QIcon(os.path.join(ICONS_DIR, "icons", "remove.png")),
            "Удалить график",
            self,
        )
        self.remove_page_act.setToolTip("Удалить график")
        self.remove_page_act.triggered.connect(self.remove_page)

        self.prev_page_act = QAction(
            QIcon(os.path.join(ICONS_DIR, "icons", "prev.png")),
            "Предыдущий график",
            self,
        )
        self.prev_page_act.setToolTip("Предыдущий график")
        self.prev_page_act.triggered.connect(self.prev_page)

        self.next_page_act = QAction(
            QIcon(os.path.join(ICONS_DIR, "icons", "next.png")),
            "Следующий график",
            self,
        )
        self.next_page_act.setToolTip("Следующий график")
        self.next_page_act.triggered.connect(self.next_page)

        self.save_all_act = QAction(
            QIcon(os.path.join(ICONS_DIR, "icons", "save_all.png")),
            "Сохранить все графики",
            self,
        )
        self.save_all_act.setToolTip("Сохранить все графики")
        self.save_all_act.triggered.connect(self.save_all)

        self.save_state_act = QAction(
            QIcon(os.path.join(ICONS_DIR, "icons", "save_state.png")),
            "Сохранить состояние",
            self,
        )
        self.save_state_act.setToolTip("Сохранить состояние")
        self.save_state_act.triggered.connect(self.save_state)

        self.load_state_act = QAction(
            QIcon(os.path.join(ICONS_DIR, "icons", "load_state.png")),
            "Загрузить состояние",
            self,
        )
        self.load_state_act.setToolTip("Загрузить состояние")
        self.load_state_act.triggered.connect(self.load_state)

        self.word_act = QAction(
            QIcon(os.path.join(ICONS_DIR, "icons", "word.png")),
            "Перенести графики в Word",
            self,
        )
        self.word_act.setToolTip("Перенести графики в Word")
        self.word_act.triggered.connect(self.export_to_word)

        self.word_settings_act = QAction(
            QIcon(os.path.join(ICONS_DIR, "icons", "settings.jpg")),
            "Настройки Word",
            self,
        )
        self.word_settings_act.setToolTip("Настройки Word")
        self.word_settings_act.triggered.connect(self.open_settings)
        self.path_lbl = QLabel("Путь к файлу:")
        self.path_lbl.setStyleSheet(
            "color: black;\n" "font-size: 14px;\n" "font-weight: 700;"
        )
        self.path_ent = MyLineEdit()
        self.path_ent.setPlaceholderText(r"C:\Users\...\res_cyclic.txt")
        self.path_ent.setMaximumWidth(600)
        self.path_ent.setAcceptDrops(True)
        self.path_ent.setStyleSheet(MY_LINE_EDIT_STYLE)
        self.path_ent.returnPressed.connect(self.load_data)
        toolbar.addAction(self.insert_page_left_act)
        toolbar.addAction(self.add_page_act)
        toolbar.addAction(self.insert_page_right_act)
        toolbar.addAction(self.remove_page_act)
        toolbar.addSeparator()
        toolbar.addAction(self.prev_page_act)
        toolbar.addAction(self.next_page_act)
        toolbar.addSeparator()
        toolbar.addAction(self.save_all_act)
        toolbar.addAction(self.save_state_act)
        toolbar.addAction(self.load_state_act)
        toolbar.addAction(self.word_act)
        toolbar.addSeparator()
        toolbar.addAction(self.word_settings_act)
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        toolbar.addWidget(spacer)
        toolbar.addWidget(self.path_lbl)
        toolbar.addWidget(self.path_ent)

    def center(self):
        """Центрирование главного окна окна"""
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        window_width = size.width()
        window_height = size.height()
        x = (screen.width() - window_width) // 2
        y = (screen.height() - window_height) // 2
        self.move(x, y)

    def showEvent(self, event):
        """Обработчик события отображения окна на экране"""
        super().showEvent(event)
        self.center()

    def change_status(self, message):
        """Изменяет текст в статусбаре"""
        self.statusBar.showMessage(str(message))

    def mousePressEvent(self, event):
        """Устанавливает фокус на главное окно при клике мышью"""
        self.setFocus()
        super().mousePressEvent(event)

    def load_data(self):
        """Загружает данные из файла, указанного в self.path_ent"""
        file_path = Path(self.path_ent.text()).resolve()
        logger.info(f"Попытка загрузки данных из файла: {file_path}")
        try:
            if file_path.suffix == ".yaml":
                with open(file_path, "r", encoding=ENCODING) as f:
                    state = yaml.load(f, Loader=yaml.FullLoader)
                    file_path = state.get("data_file_path", DEFAULT_FILE_PATH)
                    self.path_ent.setText(file_path)
            self.data = load_data_from(file_path, ENCODING)
            if isinstance(self.data, str):
                msg = MessageWindow(self.data)
                msg.exec_()
            for page in self.pages:
                for combo in page["left"].combos:
                    combo.clear()
                    combo.blockSignals(True)
                    combo._original_items = []
                    combo.addItems(self.data.columns[1:])
                    combo.setCurrentIndex(-1)
                    combo.blockSignals(False)
                page["right"].data = self.data
                page["right"].clear_graph()

                self.update_graph()
        except FileNotFoundError:
            logger.error(f"Файл данных не найден: {file_path}")
            QMessageBox.critical(self, "Ошибка", f"Файл данных не найден: {file_path}")
        except Exception as e:
            logger.error(
                f"Ошибка при загрузке данных из файла: {file_path}. Текст ошибки: {str(e)}",
                exc_info=True,
            )
            QMessageBox.critical(
                self,
                "Ошибка",
                f"Ошибка при загрузке данных из файла: {file_path}\nТекст ошибки: {str(e)}",
            )

    def export_to_word(self):
        """Экспорт всех графиков в документ Word"""
        # Запрос пути сохранения
        options = QFileDialog.Options()
        path = self.path_ent.text()
        if path:
            home_dir = Path(path).parent.as_posix()
        else:
            home_dir = os.path.expanduser(DEFAULT_DIR)
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить документ Word",
            home_dir,
            "Word Files (*.docx);;All Files (*)",
            options=options,
        )

        if not file_name:
            return
        logger.info(f"Сохранение графиков в Word в директорию: {file_name}")
        progress = MyProgressDialog(title="Сохранение документа", parent=self)
        progress.show()
        try:
            # Сохраняем текущую страницу
            original_page = self.current_page
            # Махинации с Word
            word_doc = Word()
            # Отступы
            word_doc.set_margin()
            # Основной стиль документа
            word_doc.set_style_document()
            # Стиль подрисуночной подписи
            word_doc.set_style_list(
                font=self.params.get("font", "Times New Roman"),
                font_size=self.params.get("font-size", "11"),
                line_spacing=self.params.get("line-spacing", "Одинарный"),
                int_before=self.params.get("int-before", "0"),
                int_after=self.params.get("int-after", "0"),
            )
            # Временная папка для изображений
            temp_dir = Path("./temp_grf")
            temp_dir.mkdir(exist_ok=True, parents=True)
            progress.setMaximum(len(self.pages))
            for idx, page in enumerate(self.pages):
                progress.setValue(idx)
                # Переключаемся на страницу
                self.current_page = idx
                self.stack.setCurrentIndex(idx)
                QApplication.processEvents()
                if progress.wasCanceled():
                    break
                # Обновляем график
                self.update_graph()
                page["right"].canvas.draw_idle()
                QApplication.processEvents()
                # Сохраняем временное изображение
                img_path = temp_dir / f"graph_{idx}.png"
                current_width, current_hight = page[
                    "right"
                ].canvas.fig.get_size_inches()
                page["right"].canvas.fig.set_size_inches(
                    page["right"].init_width, page["right"].init_hight
                )

                page["right"].canvas.figure.savefig(img_path, dpi=300)
                page["right"].canvas.figure.set_size_inches(
                    current_width, current_hight
                )
                # Добавляем в документ
                # 1. Изображение
                word_doc.add_image(
                    img_path,
                    pic_width=self.params.get("pic-width", "16.0"),
                    pic_height=self.params.get("pic-height", "9.5"),
                )
                # 2. Подписи к изображениям
                labels = [
                    combo.currentText().split(",")[0].strip()
                    for combo in page["left"].combos
                    if combo.currentText()
                ]
                # Используем ID графика для получения альтернативной подписи
                graph_id = page.get("id", f"graph_{idx}")
                alternative_caption = self.alternative_captions.get(graph_id)
                word_doc.set_caption(idx, labels, self.params, alternative_caption)
            # Удаляем временные файлы
            for f in temp_dir.glob("*.png"):
                f.unlink()
            temp_dir.rmdir()

            # Сохраняем документ
            if not progress.wasCanceled():
                word_doc.save_doc(file_name)
                QMessageBox.information(
                    self,
                    "Успех",
                    f"Графики успешно экспортированы в Word в директорию:\n{file_name}",
                )
                logger.info(
                    f"Графики успешно экспортированы в Word в директорию: {file_name}"
                )
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка экспорта: {str(e)}")

        finally:
            # Восстанавливаем ранее открытую страницу
            progress.close()
            self.current_page = original_page
            self.stack.setCurrentIndex(original_page)
            self.update_buttons()

    def open_settings(self):
        """Открывает окно настроек Word"""
        self.word_settings = WordSettings(parent=self)
        self.word_settings.setWindowModality(Qt.ApplicationModal)
        self.word_settings.show()

    def add_page(self):
        """Добавляет новую страницу в стек виджетов."""
        logger.info(f"Добавление страницы")
        page = QWidget()
        layout = QHBoxLayout(page)
        vlayout = QVBoxLayout()

        left_panel = LeftPanel(self.data, self)
        plot_area = PlotArea(self.data, self)

        vlayout.addWidget(left_panel, 1)
        vlayout.addStretch(10)
        layout.addLayout(vlayout, 1)
        layout.addWidget(plot_area, 4)

        page_data = {
            "widget": page,
            "left": left_panel,
            "right": plot_area,
            "id": f"graph_{len(self.pages)}"  # Добавляем уникальный ID
        }

        self.pages.append(page_data)
        self.stack.addWidget(page)
        self.current_page = len(self.pages) - 1
        self.stack.setCurrentIndex(self.current_page)
        self.pages[self.current_page]["left"].update_label()
        self.update_buttons()
        self.stack.setCurrentIndex(self.current_page)
        logger.info(f"Добавлена страница №{self.current_page + 1}")

    def remove_page(self):
        logger.info(f"Удаление страницы")
        if len(self.pages) > 1:
            page_to_remove = self.pages.pop(self.current_page)
            self.stack.removeWidget(page_to_remove["widget"])
            page_to_remove["widget"].deleteLater()
            if self.current_page >= len(self.pages):
                self.current_page = len(self.pages) - 1
            self.stack.setCurrentIndex(self.current_page)
            self.pages[self.current_page]["left"].update_label()
            self.update_buttons()
            logger.info(f"Удалена страница №{self.current_page + 1}")
        else:
            msg = MessageWindow(
                "Невозможно удалить", "Невозможно удалить последнюю страницу"
            )
            msg.exec_()

    def insert_page_right(self):
        logger.info(f"Добавление страницы")
        page = QWidget()
        layout = QHBoxLayout(page)
        vlayout = QVBoxLayout()

        left_panel = LeftPanel(self.data, self)
        plot_area = PlotArea(self.data, self)

        vlayout.addWidget(left_panel, 1)
        vlayout.addStretch(10)
        layout.addLayout(vlayout, 1)
        layout.addWidget(plot_area, 4)
        self.current_page = self.current_page + 1

        page_data = {
            "widget": page,
            "left": left_panel,
            "right": plot_area,
            "id": f"graph_{len(self.pages)}"  # Добавляем уникальный ID
        }

        self.pages.insert(self.current_page, page_data)
        self.stack.insertWidget(self.current_page, page)
        self.stack.setCurrentIndex(self.current_page)
        self.pages[self.current_page]["left"].update_label()
        self.update_buttons()
        logger.info(f"Добавлена страница №{self.current_page + 1}")

    def insert_page_left(self):
        logger.info(f"Добавление страницы")
        page = QWidget()
        layout = QHBoxLayout(page)
        vlayout = QVBoxLayout()

        left_panel = LeftPanel(self.data, self)
        plot_area = PlotArea(self.data, self)

        vlayout.addWidget(left_panel, 1)
        vlayout.addStretch(10)
        layout.addLayout(vlayout, 1)
        layout.addWidget(plot_area, 4)
        self.current_page = self.current_page

        page_data = {
            "widget": page,
            "left": left_panel,
            "right": plot_area,
            "id": f"graph_{len(self.pages)}"  # Добавляем уникальный ID
        }

        self.pages.insert(self.current_page, page_data)
        self.stack.insertWidget(self.current_page, page)
        self.stack.setCurrentIndex(self.current_page)
        self.pages[self.current_page]["left"].update_label()
        self.update_buttons()
        logger.info(f"Добавлена страница №{self.current_page + 1}")

    def update_buttons(self):
        self.prev_page_act.setEnabled(self.current_page > 0)
        self.next_page_act.setEnabled(self.current_page < len(self.pages) - 1)
        self.insert_page_left_act.setEnabled(self.current_page > 0)
        self.insert_page_right_act.setEnabled(self.current_page < len(self.pages))
        self.remove_page_act.setEnabled(len(self.pages) > 1)

    def update_graph(self):
        combos = self.pages[self.current_page]["left"].combos
        for i in range(len(combos)):
            self.plot_selection(i)

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.stack.setCurrentIndex(self.current_page)
            self.pages[self.current_page]["left"].update_label()
            self.update_buttons()
            self.update_graph()

    def next_page(self):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            self.stack.setCurrentIndex(self.current_page)
            self.pages[self.current_page]["left"].update_label()
            self.update_buttons()
            self.update_graph()

    def plot_selection(self, combo_idx: int):
        current_page = self.pages[self.current_page]
        combo = current_page["left"].combos[combo_idx]
        selected_col = combo.currentText()
        if selected_col:
            current_page["right"].update_plot(combo_idx, selected_col)
        else: 
            current_page["right"].remove_line(combo_idx)

    def save_state(self):
        options = QFileDialog.Options()
        path = SAVE_FILE.read_text()
        if path:
            home_dir = Path(path).parent.as_posix()
        else:
            home_dir = os.path.expanduser(DEFAULT_DIR)
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить состояние",
            home_dir,
            "All Files (*)",
            options=options,
        )

        if not file_name:
            return
        if not file_name.endswith(".yaml"):
            file_name = file_name + ".yaml"
        logger.info(f"Сохранение состояния в директорию: {file_name}")
        if file_name:
            path = Path(self.path_ent.text())
            state = {
                "data_file_path": path.as_posix(),
                "_Word": self.params,
                "pages": [],
            }
            for i, page_data in enumerate(self.pages):
                # Используем ID графика вместо номера
                graph_id = page_data.get("id", f"graph_{i}")
                # Получаем альтернативную подпись из self.alternative_captions
                alternative_caption = self.alternative_captions.get(graph_id, "")
                page_state = {
                    "id": graph_id,
                    "Symbol_Y": [
                        str(page_data["right"].group.currentText()),
                        str(page_data["right"].sizing_cmb.currentText()),
                    ],
                    "Symbol_X": [
                        str(page_data["right"].group_x.currentText()),
                        str(page_data["right"].sizing_cmb_x.currentText()),
                    ],
                    "Axis_settings": {
                        "X": str(page_data["right"].x_settings.currentText()),
                        "Y": str(page_data["right"].y_settings.text()),
                        "Frequency": str(page_data["right"].markers.currentText()),
                        "X_grid_lines": str(
                            page_data["right"].x_spacing_grid_spinBox.value()
                        ),
                    },
                    "Lists": [],
                    "alternative_caption": alternative_caption,
                }
                for combo in page_data["left"].combos:
                    text = combo.currentText()
                    page_state["Lists"].append(text)
                state["pages"].append(page_state)

            with open(file_name, "w", encoding="cp1251") as f:
                yaml.dump(state, f, indent=2, allow_unicode=True)
            self.write_path(file_name)
            logger.info(f"Состояние успешно сохранено в директорию {file_name}")

    def _load_state(self, file_path=SAVE_FILE.read_text()):
        logger.info("Загрузка состояния...")
        try:
            logger.debug("Загрузка состояния...")
            progress = MyProgressDialog(title="Загрузка состояния", parent=self)
            progress.show()
            QApplication.processEvents()

            with open(file_path, "r", encoding=ENCODING) as f:
                state = yaml.load(f, Loader=yaml.FullLoader)

            # 1. Очистка текущего состояния
            while self.pages:
                page = self.pages.pop()
                self.stack.removeWidget(page["widget"])
                QApplication.processEvents()

            # 2. Загрузка данных
            self.path_ent.blockSignals(True)
            self.data_file_path = state.get("data_file_path", DEFAULT_FILE_PATH)
            self.params = state.get("_Word", {})
            self.path_ent.setText(self.data_file_path)
            self.path_ent.blockSignals(False)
            self.data = load_data_from(self.data_file_path, ENCODING)
            if isinstance(self.data, str):
                msg = MessageWindow(self.data)
                msg.exec_()
                raise Exception
            self.alternative_captions = {}

            # 3. Воссоздание страниц
            total_pages = len(state.get("pages", []))
            progress.setMaximum(total_pages)
            for i, page_state in enumerate(state.get("pages", [])):
                progress.setValue(i)
                progress.setLabelText(f"Загрузка страницы {i}/{total_pages}")
                QApplication.processEvents()

                if progress.wasCanceled():
                    break

                self.current_page = 0
                self.add_page()
                current_page = self.pages[-1]

                # Устанавливаем ID графика
                current_page["id"] = page_state.get("id", f"graph_{i}")

                # Загрузка параметров правой части
                current_page["right"].x_settings.setCurrentText(
                    page_state["Axis_settings"]["X"]
                )
                current_page["right"].y_settings.setText(
                    page_state["Axis_settings"]["Y"]
                )
                current_page["right"].markers.setCurrentText(
                    page_state["Axis_settings"]["Frequency"]
                )
                current_page["right"].x_spacing_grid_spinBox.setValue(
                    int(page_state["Axis_settings"]["X_grid_lines"])
                )
                current_page["right"].group.setCurrentText(page_state["Symbol_Y"][0])
                current_page["right"].sizing_cmb.setCurrentText(
                    page_state["Symbol_Y"][1]
                )
                current_page["right"].group_x.setCurrentText(page_state["Symbol_X"][0])
                current_page["right"].sizing_cmb_x.setCurrentText(
                    page_state["Symbol_X"][1]
                )

                # Загрузка параметров левой части
                for j, combo_text in enumerate(page_state["Lists"]):
                    if j < len(current_page["left"].combos):
                        current_page["left"].combos[j].setCurrentText(combo_text)

                # Загрузка альтернативной подписи по ID
                graph_id = page_state.get("id", f"graph_{i}")
                self.alternative_captions[graph_id] = page_state.get(
                    "alternative_caption", ""
                )
                self.update_graph()
                QApplication.processEvents()

            # 4. Восстановление позиции
            if self.pages:
                self.current_page = 0
                self.stack.setCurrentIndex(0)
                self.update_buttons()
                self.pages[0]["left"].update_label()
            self.write_path(file_path)
            self.change_status(file_path)
            logger.info("Состояние успешно загружено")

        except Exception as e:
            if isinstance(e, FileNotFoundError):
                return
            else:
                QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки: {str(e)}")
            logger.error(f"Ошибка при загрузке состояния: {str(e)}", exc_info=True)
        finally:
            progress.close()

    def load_state(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        path = Path(self.path_ent.text()).resolve()
        if path:
            home_dir = Path(path).parent.as_posix()
        else:
            home_dir = os.path.expanduser(DEFAULT_DIR)

        self.state_file_path, _ = QFileDialog.getOpenFileName(
            self, "Загрузить состояние", home_dir, "All Files (*)", options=options
        )
        if self.state_file_path != "":
            try:
                self._load_state(self.state_file_path)

            except Exception as e:
                msg = MessageWindow(
                    f"Ошибка загрузки состояния из файла:\n{self.state_file_path}",
                    f"Текст ошибки: {str(e)}",
                )
                msg.exec_()

    def save_all(self):
        """Сохраняет все графики в выбранную пользователем директорию."""
        # Запрос директории сохранения
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly  # Показываем только папки
        # options |= QFileDialog.DontUseNativeDialog
        path = self.path_ent.text()
        if path:
            home_dir = Path(path).parent.as_posix()
        else:
            home_dir = os.path.expanduser(DEFAULT_DIR)
        directory = QFileDialog.getExistingDirectory(
            self, "Выберите папку для сохранения графиков", home_dir, options=options
        )

        if not directory:
            return  # Пользователь отменил выбор

        logger.info(f"Сохранение всех графиков в директорию: {directory}")
        # Сохраняем текущую активную страницу
        original_page = self.current_page
        try:
            # Создаем папку если нужно
            for idx, page in enumerate(self.pages):
                self.current_page = idx
                self.stack.setCurrentIndex(idx)

                # Обновляем интерфейс страницы
                QApplication.processEvents()

                # Принудительно обновляем графики
                self.update_graph()
                page["left"].update_label()
                page["right"].canvas.draw_idle()
                QApplication.processEvents()

                number = (
                    page["left"].num_page.text().replace(" ", "_").replace("/", "-")
                )
                filename = os.path.join(directory, f"{number}.png")
                current_width, current_hight = page[
                    "right"
                ].canvas.fig.get_size_inches()
                page["right"].canvas.fig.set_size_inches(
                    page["right"].init_width, page["right"].init_hight
                )

                page["right"].canvas.figure.savefig(
                    filename,
                    format="png",
                    dpi=300,
                )
                page["right"].canvas.figure.set_size_inches(
                    current_width, current_hight
                )
            QMessageBox.information(
                self, "Успешно", f"Графики сохранены в:\n{directory}"
            )
            self.update_buttons()
            self.current_page = original_page
            self.stack.setCurrentIndex(original_page)
            logger.info(f"Успешное сохранение всех графиков в директорию: {directory}")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка сохранения: {str(e)}")
            logger.error(
                f"Ошибка при сохранении всех графиков: {str(e)}", exc_info=True
            )
        finally:
            self.current_page = original_page
            self.stack.setCurrentIndex(original_page)
            self.update_buttons()

    def write_path(self, path):
        """Перезаписывает путь к последнему файлу состояния"""
        with open(SAVE_FILE, "w", encoding="cp1251") as f:
            f.write(path)

    def new_project(self):
        """Создание нового проекта"""
        reply = QMessageBox.question(
            self,
            "Вы уверены?",
            f"Вы уверены, что хотите создать новый проект?\nВсе несохраненные данные будут утеряны!",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self.clear_all()
            self.pages = []
            self.add_page()
            self.path_ent.clear()
            [i.clear() for i in self.pages[0]["left"].combos]
            self.pages[0]["left"].combos[0].clear()
        else:
            return

    def clear_all(self):
        """Очистка главного окна от всех виджетов"""
        for page in self.pages:
            self.stack.removeWidget(page["widget"])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
