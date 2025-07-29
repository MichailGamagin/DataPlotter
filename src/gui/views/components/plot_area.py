import os
import math
from pathlib import Path

import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QComboBox,
    QPushButton,
    QLabel,
    QLineEdit,
    QMessageBox,
    QFileDialog,
    QSpinBox,
    QSizePolicy,
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon

from src.core.constants import (
    MAIN_CHARS,
    UNITS,
    SIZING,
    COLORS,
    DEFAULT_DIR,
    MARKERS,
    ICONS_DIR,
)
from src.gui.styles import COMBO_STYLE, LINE_EDIT_STYLE, LABEL_STYLE, SPIN_BOX_STYLE

from src.gui.views.components.toolbar import MyNavigationToolbar
from src.gui.views.dialogs.message import MessageWindow
from src.utils.logger import Logger

logger = Logger.get_logger(__name__)


class PlotCanvas(FigureCanvas, QWidget):
    """
    Виджет для отображения графика.

    Attributes:
        fig (Figure): Объект фигуры matplotlib.
        ax (Axes): Объект осей matplotlib.
    """

    def __init__(self, parent=None):
        """
        Инициализация виджета графика.

        Args:
            parent: Родительский виджет.
        """
        logger.info("Инициализация PlotCanvas")
        self.fig = Figure(figsize=(9, 5))
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.ax.grid(
            True,
            which="major",
            axis="both",
            linestyle="-",
            linewidth=0.5,
            color="black",
        )
        self.setParent(parent)
        logger.info("Инициализация PlotCanvas успешно завершена")

    def clear_plot(self):
        """Метод очистки графика"""
        self.ax.cla()
        self.ax.grid(
            True,
            which="major",
            axis="both",
            linestyle="-",
            linewidth=0.5,
            color="black",
        )
        self.draw()


class PlotArea(QWidget):
    """
    Виджет для отображения правой части интерфейса.

    Attributes:
        lines (dict): Словарь, хранящий объекты линий на графике.
        data (pd.DataFrame): Данные для построения графика.
        main_window (QMainWindow): Ссылка на главное окно приложения.
        marker_freq (int): Частота маркеров на графике.
        canvas (PlotCanvas): Холст для рисования графика.
        toolbar (MyNavigationToolbar): Панель инструментов для навигации по графику.
        clear_btn (QPushButton): Кнопка для очистки графика.
        save_btn (QPushButton): Кнопка для сохранения графика.
        group (QComboBox): Выпадающий список для выбора обозначения оси Y.
        sizing_cmb (QComboBox): Выпадающий список для выбора размерности оси Y.
        x_settings (QComboBox): Выпадающий список для настройки оси X.
        y_settings (QLineEdit): Поле ввода для настройки оси Y.
        markers (QComboBox): Выпадающий список для настройки частоты маркеров.
        x_axis_limit (int): Предел оси X.
    """

    def __init__(self, data: pd.DataFrame, main_window, parent=None):
        super().__init__(parent)
        logger.info("Инициализация PlotArea")
        self.lines = {}
        self.data = data
        self.main_window = main_window
        self.init_ui()
        logger.info("Инициализация PlotArea успешно завершена")

    def init_ui(self):
        logger.info("Инициализация пользовательского интерфейса PlotArea")
        self.main_layout = QVBoxLayout(self)
        # Top controls
        self.top_controls_panel = QWidget()
        self.top_controls_panel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.top_controls_layout = QGridLayout(self.top_controls_panel)
        self.top_controls_layout.setContentsMargins(0, 0, 0, 0)
        self.top_controls_layout.setVerticalSpacing(10)
        self.top_controls_layout.setHorizontalSpacing(10)
        # Создаем виджеты
        # Обозначение оси Y
        group_lbl_y = QLabel("Обозначение Y:")
        group_lbl_y.setToolTip(
            "Буквенное обозначение\nфизической величины.\nНапример: Q, P, T и т.д."
        )
        group_lbl_y.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        group_lbl_y.setStyleSheet(LABEL_STYLE)
        self.group = QComboBox()
        self.group.addItems(MAIN_CHARS)
        self.group.setStyleSheet(COMBO_STYLE)
        self.group.setEditable(True)
        self.group.setCurrentIndex(-1)
        self.group.currentTextChanged.connect(self.main_window.update_graph)
        # Размерность
        sizing_lbl_y = QLabel("Размерность Y:")
        sizing_lbl_y.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sizing_lbl_y.setStyleSheet(LABEL_STYLE)
        self.sizing_cmb = QComboBox()
        self.sizing_cmb.setStyleSheet(COMBO_STYLE)
        self.sizing_cmb.addItems(SIZING)
        self.sizing_cmb.setEditable(True)
        self.sizing_cmb.setCurrentIndex(-1)
        self.sizing_cmb.currentTextChanged.connect(self.main_window.update_graph)
        # Настройка оси X
        x_ax_settings_lbl = QLabel("Настройка оси X:")
        x_ax_settings_lbl.setToolTip(
            "Разрешенный тип данных - int\nПример: 'auto', '100', '300'"
        )
        x_ax_settings_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        x_ax_settings_lbl.setStyleSheet(LABEL_STYLE)
        self.x_settings = QComboBox()
        self.x_settings.setStyleSheet(COMBO_STYLE)
        self.x_settings.addItems(["auto", "300", "600", "1800", "3600"])
        self.x_settings.setEditable(True)
        self.x_settings.setCurrentIndex(0)
        self.x_settings.currentTextChanged.connect(self.main_window.update_graph)
        group_lbl_x = QLabel("Обозначение X:")
        group_lbl_x.setToolTip("Буквенное обозначение времени.\nНапример: t")
        group_lbl_x.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        group_lbl_x.setStyleSheet(LABEL_STYLE)
        sizing_lbl_x = QLabel("Размерность X:")
        sizing_lbl_x.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sizing_lbl_x.setStyleSheet(LABEL_STYLE)
        self.sizing_cmb_x = QComboBox()
        self.sizing_cmb_x.setStyleSheet(COMBO_STYLE)
        self.sizing_cmb_x.addItems(["t", "tau"])
        self.sizing_cmb_x.setEditable(True)
        self.sizing_cmb_x.currentTextChanged.connect(self.main_window.update_graph)
        self.sizing_cmb_x.setCurrentIndex(0)
        self.group_x = QComboBox()
        self.group_x.addItems(["s", "с", "h", "ч"])
        self.group_x.setStyleSheet(COMBO_STYLE)
        self.group_x.setEditable(True)
        self.group_x.currentTextChanged.connect(self.main_window.update_graph)
        self.group_x.setCurrentIndex(0)
        # Настройка оси Y
        y_ax_settings_lbl = QLabel("Настройка оси Y:")
        y_ax_settings_lbl.setToolTip("Формат: min,max или auto\nПример: '0,100.5'")
        y_ax_settings_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        y_ax_settings_lbl.setStyleSheet(LABEL_STYLE)
        self.y_settings = QLineEdit()
        self.y_settings.setText("auto")
        self.y_settings.setStyleSheet(LINE_EDIT_STYLE)
        self.y_settings.editingFinished.connect(self.change_y_settings)
        # Распределение элементов по сетке
        self.top_controls_layout.addWidget(y_ax_settings_lbl, 0, 0, 1, 1)
        self.top_controls_layout.addWidget(self.y_settings, 0, 1, 1, 1)
        self.top_controls_layout.addWidget(group_lbl_y, 1, 0, 1, 1)
        self.top_controls_layout.addWidget(self.group, 1, 1, 1, 1)
        self.top_controls_layout.addWidget(sizing_lbl_y, 2, 0, 1, 1)
        self.top_controls_layout.addWidget(self.sizing_cmb, 2, 1, 1, 1)
        self.top_controls_layout.addWidget(x_ax_settings_lbl, 0, 2, 1, 1)
        self.top_controls_layout.addWidget(self.x_settings, 0, 3, 1, 1)
        self.top_controls_layout.addWidget(group_lbl_x, 1, 2, 1, 1)
        self.top_controls_layout.addWidget(sizing_lbl_x, 2, 2, 1, 1)
        self.top_controls_layout.addWidget(self.sizing_cmb_x, 1, 3, 1, 1)
        self.top_controls_layout.addWidget(self.group_x, 2, 3, 1, 1)
        marker_lbl = QLabel("Частота маркера:")
        marker_lbl.setToolTip("Устанавливает частоту маркеров\nна всех линиях графика")
        marker_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        marker_lbl.setStyleSheet(LABEL_STYLE)
        self.markers = QComboBox()
        self.markers.setStyleSheet(COMBO_STYLE)
        self.markers.addItems(["auto", "300", "600", "2000", "3000"])
        self.markers.setEditable(True)
        self.markers.setCurrentIndex(0)
        self.markers.currentTextChanged.connect(self.update_marker_frequency)
        x_spacing_grid_lbl = QLabel("Линии сетки:")
        x_spacing_grid_lbl.setToolTip(
            "Устанавливает количество вертикальных\nлиний сетки на графике"
        )
        x_spacing_grid_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        x_spacing_grid_lbl.setStyleSheet(LABEL_STYLE)
        self.x_spacing_grid_spinBox = QSpinBox()
        self.x_spacing_grid_spinBox.setValue(4)
        self.x_spacing_grid_spinBox.setMinimum(2)
        self.x_spacing_grid_spinBox.setStyleSheet(SPIN_BOX_STYLE)
        self.x_spacing_grid_spinBox.valueChanged.connect(self.change_x_settings)
        self.top_controls_layout.addWidget(marker_lbl, 0, 4, 1, 1)
        self.top_controls_layout.addWidget(self.markers, 0, 5, 1, 1)
        self.top_controls_layout.addWidget(x_spacing_grid_lbl, 1, 4, 1, 1)
        self.top_controls_layout.addWidget(self.x_spacing_grid_spinBox, 1, 5, 1, 1)
        # Добавляем панель в основной макет
        self.main_layout.addWidget(self.top_controls_panel)
        # Plot area
        self.bottom_panel = QWidget()
        self.plot_layout = QVBoxLayout(self.bottom_panel)
        # Новая панель для тулбара и кнопок
        self.toolbar_and_buttons_panel = QWidget()
        self.toolbar_and_buttons_layout = QHBoxLayout(self.toolbar_and_buttons_panel)
        self.toolbar_and_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.canvas = PlotCanvas()
        self.canvas.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.toolbar = MyNavigationToolbar(
            self.canvas, self.canvas, self, coordinates=False
        )
        self.clear_btn = QPushButton()
        self.clear_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "icons", "clear.png")))
        self.clear_btn.setToolTip("Очистить график")
        self.clear_btn.setMaximumWidth(50)
        self.save_btn = QPushButton()
        self.save_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "icons", "save.png")))
        self.save_btn.setToolTip("Сохранить график")
        self.save_btn.setMaximumWidth(50)
        self.toolbar.setFixedWidth(150)
        self.clear_btn.clicked.connect(self.clear_graph)
        self.save_btn.clicked.connect(self.save)
        self.plot_layout.addWidget(self.canvas)
        # Добавляем toolbar и кнопки в новую панель
        self.toolbar_and_buttons_layout.addWidget(self.toolbar)
        self.toolbar_and_buttons_layout.addStretch(1)
        self.toolbar_and_buttons_layout.addWidget(self.clear_btn)
        self.toolbar_and_buttons_layout.addWidget(self.save_btn)
        self.plot_layout.addWidget(self.toolbar_and_buttons_panel)
        self.main_layout.addWidget(self.bottom_panel)
        self.init_width, self.init_hight = self.canvas.fig.get_size_inches()
        logger.info(
            "Инициализация пользовательского интерфейса PlotArea успешно завершена"
        )

    def update_marker_frequency(self):
        """
        Обновляет частоту маркеров при изменении значения в комбобоксе.
        """
        text = self.markers.currentText()
        ax = self.canvas.ax
        if text.isdigit() and int(text) > 0:
            self.marker_freq = int(text)
            self.redraw_markers()
        elif text in "auto" or text.startswith("0"):
            self.marker_freq = int(ax.get_xlim()[1] / 10)
            self.redraw_markers()
        else:
            QMessageBox.warning(
                self,
                "Неверный формат",
                "Пожалуйста, введите целое положительное число или выберите 'auto'.",
            )
            self.markers.setCurrentIndex(0)  # Сбрасываем на 'auto'
            return

    def redraw_markers(self):
        """Перерисовывает маркеры на всех существующих линиях."""
        markers = MARKERS
        ax = self.canvas.ax
        quantity_lines = len(self.lines)
        if quantity_lines == 1:
            line = list(self.lines.values())[0]
        elif quantity_lines > 1:
            step = int(math.sqrt(self.marker_freq))
            for line_idx, line in self.lines.items():
                markevery = self.marker_freq + line_idx * step
                line.set_marker(markers[line_idx])
                line.set_markevery(markevery)
        handles, labels = ax.get_legend_handles_labels()
        if quantity_lines >= 7:
            ncols = 2
            fz = 9
        else:
            ncols = 1
            fz = 10
        if len(handles) > 1:
            ax.legend(handles, labels, fontsize=fz, ncols=ncols)
        else:
            ax.legend().remove()
        ax.tick_params(axis="both", which="major", labelsize=12)
        self.canvas.draw_idle()

    def get_current_params(self):
        """
        Получает текущие выбранные параметры из выпадающих списков.
        """
        params = []
        for combo in self.main_window.pages[self.main_window.current_page][
            "left"
        ].combos:
            params.append(combo.currentText())
        return params

    def vis_x_label_text(self):
        unit = self.sizing_cmb_x.currentText()
        if unit == "":
            unit_tex = ""
        else:
            unit_tex = r"\text{" + unit + "}"
        char = self.group_x.currentText()
        if char == "":
            char_tex = ""
        else:
            char_tex = r"\text{" + char + "}"
        if char_tex != "" and unit_tex != "":
            x_label_text = rf"$\frac{{{unit_tex}}}{{{char_tex}}}$"
        elif char_tex != "" and unit_tex == "":
            x_label_text = rf"${char_tex}$"
        elif char_tex == "" and unit_tex != "":
            x_label_text = rf"${unit_tex}$"
        else:
            x_label_text = ""
        return x_label_text

    def vis_y_label_text(self):
        """
        Формирует текст в формате Latex для подписи оси Y .
        """
        greek_alf = {
            "alpha": r"\alpha",
            "beta": r"\beta",
            "gamma": r"\gamma",
            "delta": r"\delta",
            "pi": r"\pi",
            "rho": r"\rho",
            "tau": r"\tau",
            "phi": r"\phi",
            "omega": r"\omega",
            "DeltaC": r"\Delta C",
            "Phi": r"\Phi",
        }

        units = UNITS
        unit = self.sizing_cmb.currentText()
        if unit in units:
            unit_tex = units[unit]
        elif unit == "":
            unit_tex = ""
        else:
            unit_tex = (
                r"\text{" + unit + "}"
            )  # Если пользователь ввел свое значение, экранируем его как текст.
        char = self.group.currentText()
        if char == "":
            char_tex = ""
        elif char in greek_alf.keys():
            char_tex = f"{greek_alf[char]}"
        else:
            char_tex = r"\text{" + char + "}"

        if char_tex != "" and unit_tex != "":
            y_label_text = rf"$\frac{{{char_tex}}}{{{unit_tex}}}$"
        elif char_tex != "" and unit_tex == "":
            y_label_text = rf"${char_tex}$"
        elif char_tex == "" and unit_tex != "":
            y_label_text = rf"${unit_tex}$"
        else:
            y_label_text = ""
        return y_label_text

    def update_plot(self, line_idx: int, column_name: str):
        """
        Обновляет график с учетом выбранных параметров.

        Args:
            line_idx (int): Индекс линии, которую нужно обновить.
            column_name (str): Имя столбца данных для построения графика.
        """
        if not column_name:
            return

        colors = COLORS
        ax = self.canvas.ax
        ax.tick_params(axis="both", which="major", labelsize=12)
        ax.xaxis.label.set_fontsize(14)
        ax.yaxis.label.set_fontsize(14)
        x_label_text = self.vis_x_label_text()
        ax.set_xlabel(x_label_text, loc="right")
        y_label_text = self.vis_y_label_text()
        ax.set_ylabel(
            y_label_text,
            loc="top",
            rotation=0,
            labelpad=-10,
        )
        time = self.data.columns[0]
        self.change_x_settings()
        self.change_y_settings()
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda val, loc: f"{val:.0f}"))
        ax.yaxis.set_major_formatter(
            plt.ScalarFormatter(useMathText=True, useOffset=False)
        )

        # Remove existing line if present
        if line_idx in self.lines:
            self.lines[line_idx].remove()
            del self.lines[line_idx]
        ax.relim()
        ax.autoscale_view()
        x = self.data[time]
        if column_name in self.data.columns:
            y = self.data[column_name]
        else:
            return
        (line,) = ax.plot(
            x,
            y,
            label=str(line_idx + 1),
            color=colors[line_idx % len(colors)],
            linewidth=1.5,
        )
        self.lines[line_idx] = line
        # Update legend
        handles, labels = ax.get_legend_handles_labels()
        if len(handles) > 1:
            ax.legend(handles, labels, fontsize=10)
        else:
            ax.legend().remove()
        ax.grid(True, which="major", axis="both", linestyle="-", linewidth=0.5)
        self.update_marker_frequency()
        self.canvas.draw_idle()
        QTimer.singleShot(0, self.toolbar.save_current_view)

    def change_x_settings(self):
        """Обработчик события изменения границ оси Х"""
        ax = self.canvas.ax
        time = self.data.columns[0]
        try:
            text = self.x_settings.currentText()
            if text.isalpha() or text == "":
                self.x_axis_limit = self.data[time].max()
                ax.set_xlim(0.0, self.x_axis_limit)
            else:
                self.x_axis_limit = int(text)
                ax.set_xlim(0.0, self.x_axis_limit)
            ax.xaxis.set_major_locator(
                plt.MultipleLocator(
                    self.x_axis_limit / self.x_spacing_grid_spinBox.value()
                )
            )
            self.canvas.draw_idle()
        except ValueError:
            msg = MessageWindow(
                "Неверный формат ввода оси Х",
                "Проверьте правильность ввода\n и (возможно) файл save.yaml",
            )
            msg.exec_()
            self.x_settings.setCurrentIndex(0)
            return

    def change_y_settings(self):
        """Обработчик события изменения границ оси У"""
        ax = self.canvas.ax
        try:
            text = self.y_settings.text().strip().lower()
            if text in ["auto", ""]:
                ax.set_ylim(auto=True)
                self.y_settings.setText("auto")
            else:
                max_y = float(self.y_settings.text().split(",")[1])
                min_y = float(self.y_settings.text().split(",")[0])
                ax.set_ylim(min_y, max_y)
            self.canvas.draw_idle()
        except Exception as e:
            print(str(e))
            msg = MessageWindow(
                "Неверный диапазон оси Y",
                "Проверьте правильность ввода\nи (возможно) файл save.yaml",
            )
            msg.exec_()
            self.y_settings.setText("auto")
            return

    def clear_graph(self):
        """Обработчик события нажатия на кнопку Очистить график"""
        self.canvas.clear_plot()
        self.lines = {}
        for combo in self.main_window.pages[self.main_window.current_page][
            "left"
        ].combos:
            combo.setCurrentIndex(-1)
        right_panel = self.main_window.pages[self.main_window.current_page]["right"]
        right_panel.group.setCurrentIndex(-1)
        right_panel.sizing_cmb.setCurrentIndex(-1)
        right_panel.y_settings.setText("auto")
        right_panel.x_settings.setCurrentText("auto")
        right_panel.markers.setCurrentText("auto")
        self.canvas.draw()

    def save(self):
        """Обработчик события нажатия на кнопку Сохранить график"""
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        path = (
            self.main_window.path_ent.text()
            if self.main_window.path_ent.text()
            else DEFAULT_DIR
        )
        home_dir = Path(path).parent.as_posix()
        try:
            directory = QFileDialog.getExistingDirectory(
                self, "Выберите папку для сохранения графикa", home_dir, options=options
            )
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка в пути сохранения")
            msg.setWindowTitle("Ошибка")
            msg.setDetailedText(f"Текст ошибки: {str(e)}")
            msg.exec_()
            return
        if not directory:
            return
        if not Path(directory).exists():
            Path(directory).mkdir(exist_ok=True)
        number = self.main_window.current_page + 1
        x_axis_limit = self.canvas.ax.get_xlim()[1]

        current_width, current_hight = self.canvas.fig.get_size_inches()
        self.canvas.fig.set_size_inches(self.init_width, self.init_hight)

        filename = (
            f"/grf_{number} из {len(self.main_window.pages)}_{int(x_axis_limit)}s.png"
        )
        self.canvas.figure.savefig(directory + filename, format="png", dpi=600)
        self.canvas.figure.set_size_inches(current_width, current_hight)
        QMessageBox.information(
            self,
            "Успех",
            f"График успешно сохранен в директорию:\n{directory + filename}",
        )
        logger.info(f"График успешно сохранен в директорию: {directory + filename}")

    def remove_line(self, combo_idx: int):
        """Удаляет линию по индексу комбобокса"""
        if not self.lines:
            return
        if combo_idx in self.lines:
            line = self.lines[combo_idx]
            line.remove()
            del self.lines[combo_idx]
        handles, labels = self.canvas.ax.get_legend_handles_labels()
        if len(handles) > 1:
            if len(handles) >=7:
                ncols = 2
                fz = 9
            else:
                ncols = 1
                fz = 10
            self.canvas.ax.legend(handles, labels, fontsize = fz, ncols = ncols)
        else:
            if not self.lines:
                self.canvas.draw_idle()
                return
            line = list(self.lines.values())[0]
            line.set_markevery(10e6)
            self.canvas.ax.legend().remove()
        self.canvas.draw_idle()

    def disconnect_signals(self):
        self.group.currentTextChanged.disconnect()
        self.group_x.currentTextChanged.disconnect()
        self.x_settings.currentTextChanged.disconnect()
        self.sizing_cmb_x.currentTextChanged.disconnect()
        self.sizing_cmb.currentTextChanged.disconnect()

    def connect_signals(self):
        self.group.currentTextChanged.connect(self.main_window.update_graph)
        self.group_x.currentTextChanged.connect(self.main_window.update_graph)
        self.x_settings.currentTextChanged.connect(self.main_window.update_graph)
        self.sizing_cmb_x.currentTextChanged.connect(self.main_window.update_graph)
        self.sizing_cmb.currentTextChanged.connect(self.main_window.update_graph)
