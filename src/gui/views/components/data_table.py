import os
from typing import Optional, Any, Callable

import pandas as pd
import numpy as np
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QAbstractTableModel, pyqtSignal
from PyQt5.QtWidgets import (
    QMenu,
    QAction,
    QInputDialog,
    QMessageBox,
    QHeaderView,
    QTableView,
)
from PyQt5.QtGui import QIcon

from src.utils.logger import Logger
from src.core.constants import ICONS_DIR

logger = Logger.get_logger(__name__)


class DataOperations:
    """Класс для выполнения операций над данными"""

    @staticmethod
    def add_columns(df: pd.DataFrame, col1: str, col2: str) -> pd.Series:
        """Сложение столбцов"""
        return df[col1] + df[col2]

    @staticmethod
    def subtract_columns(df: pd.DataFrame, col1: str, col2: str) -> pd.Series:
        """Вычитание столбцов"""
        return df[col1] - df[col2]

    @staticmethod
    def add_constant(df: pd.DataFrame, col1: str, constant: np.float64) -> pd.Series:
        """Сложение столбца с константой"""
        return df[col1] + constant

    @staticmethod
    def subtract_constant(
        df: pd.DataFrame, col1: str, constant: np.float64
    ) -> pd.Series:
        """Вычитание столбца с константой"""
        return df[col1] - constant

    @staticmethod
    def multiply_constant(
        df: pd.DataFrame, col1: str, constant: np.float64
    ) -> pd.Series:
        """Умножение столбца с константой"""
        return df[col1] * constant

    @staticmethod
    def divide_constant(df: pd.DataFrame, col1: str, constant: np.float64) -> pd.Series:
        """Деление столбца с константой"""
        return df[col1] / constant

    @staticmethod
    def integral(df: pd.DataFrame, time_col: str, param_col: str) -> pd.Series:
        """
        Вычисляет интеграл параметра по времени
        """
        try:
            result = []
            for i in range(len(df)):
                area = np.trapezoid(
                    y=df[param_col].values[: i + 1], x=df[time_col].values[: i + 1]
                )
                result.append(area)
            return pd.Series(result, index=df.index, name=f"Интеграл_{param_col}")

        except Exception as e:
            logger.error(f"Ошибка при вычислении интеграла: {str(e)}")
            return pd.Series([], name=f"Интеграл_{param_col}")

    @staticmethod
    def horizontal(df: pd.DataFrame, const: np.float64) -> pd.Series:
        arr = np.full(shape=df.shape[0], fill_value=np.float64(const))
        return pd.Series(data=arr, name=str(const))


class DataModel(QAbstractTableModel):
    """
    Виджет для отображения данных в формате таблицы.

    Attributes:
        _data (pd.DataFrame): DataFrame содержащий данные для отображения
        _operations (DataOperations): Класс для выполнения операций над данными
    """

    dataChanged = pyqtSignal()

    def __init__(self, data: pd.DataFrame):
        super().__init__()
        self._data = data
        self._operations = DataOperations()
        self._init_context_menu()

    def _init_context_menu(self) -> None:
        """Инициализация контекстного меню"""
        self.context_menu = QMenu()
        # Подменю для арифметических операций
        self.arithmetic_menu = QMenu("Арифметические операции")
        self.arithmetic_menu.setIcon(
            QIcon(os.path.join(ICONS_DIR, "icons", "arifmetic50x50.png"))
        )
        # Действия для операций
        self.add_constant_action = QAction(
            QIcon(os.path.join(ICONS_DIR, "icons", "plus-64.png")),
            "Сложить с константой",
            self,
        )
        self.subtract_constant_action = QAction(
            QIcon(os.path.join(ICONS_DIR, "icons", "minus-48.png")),
            "Вычесть константу",
            self,
        )
        self.add_action = QAction(
            QIcon(os.path.join(ICONS_DIR, "icons", "add_col-48.png")),
            "Сложить с другим столбцом",
            self,
        )
        self.subtract_action = QAction(
            QIcon(os.path.join(ICONS_DIR, "icons", "sub_col-48.png")),
            "Вычесть другой столбец",
            self,
        )
        self.integral_action = QAction(
            QIcon(os.path.join(ICONS_DIR, "icons", "integral-50.png")),
            "Интеграл столбца",
            self,
        )
        self.multiply_constant_action = QAction(
            QIcon(os.path.join(ICONS_DIR, "icons", "multiply-64.png")),
            "Умножить на константу",
            self,
        )
        self.divide_constant_action = QAction(
            QIcon(os.path.join(ICONS_DIR, "icons", "divide-60.png")),
            "Разделить на константу",
            self,
        )
        self.hor_line_action = QAction(
            QIcon(os.path.join(ICONS_DIR, "icons", "")), "Горизонтальная линия", self
        )
        # Добавление действий в подменю
        self.arithmetic_menu.addAction(self.add_constant_action)
        self.arithmetic_menu.addAction(self.subtract_constant_action)
        self.arithmetic_menu.addAction(self.multiply_constant_action)
        self.arithmetic_menu.addAction(self.divide_constant_action)
        self.arithmetic_menu.addAction(self.add_action)
        self.arithmetic_menu.addAction(self.subtract_action)
        self.arithmetic_menu.addAction(self.integral_action)
        # Добавление подменю в основное меню
        self.context_menu.addMenu(self.arithmetic_menu)
        self.context_menu.addAction(self.hor_line_action)

    def add_column(self, column_name: str, data: pd.Series) -> None:
        """Добавление нового столбца в таблицу"""
        last_column = self.columnCount()
        self.beginInsertColumns(QtCore.QModelIndex(), last_column, last_column)
        self._data[column_name] = data
        self.endInsertColumns()

    def perform_operation(
        self, operation: Callable, col1: str, col2: str = None, power: float = None
    ) -> None:
        """Выполнение операции над столбцами"""
        try:
            result = operation(self._data, col1, col2)
            if operation == self._operations.add_columns:
                new_col_name = f"$({col1})+({col2})$"
            elif operation == self._operations.subtract_columns:
                new_col_name = f"$({col1})-({col2})$"
            else:
                new_col_name = f"{col1}_{operation.__name__}_{col2}"
            # Добавляем новый столбец с результатом
            self.add_column(new_col_name, result)
            self.dataChanged.emit()
        except Exception as e:
            QMessageBox.warning(
                None, "Ошибка", f"Ошибка при выполнении операции: {str(e)}"
            )
            logger.error(f"Ошибка при выполнении операции: {str(e)}")

    def perform_constant_operation(
        self, operation: Callable, col1: str, constant: float
    ) -> None:
        """Выполнение операции с константой"""
        result = operation(self._data, col1, constant)
        if operation == self._operations.add_constant:
            new_col_name = f"$({col1})+({constant})$"
        elif operation == self._operations.subtract_constant:
            new_col_name = f"$({col1})-({constant})$"
        elif operation == self._operations.multiply_constant:
            new_col_name = f"$({col1})*({constant})$"
        elif operation == self._operations.divide_constant:
            new_col_name = f"$({col1})/({constant})$"
        else:
            new_col_name = f"{col1}_{operation.__name__}_{constant}"
        self.add_column(new_col_name, result)
        self.dataChanged.emit()

    def perform_horizontal(self, operation: Callable, constant: float):
        result = operation(self._data, constant)
        if operation == self._operations.horizontal:
            new_col_name = f"$Horizontal({constant})$"
        self.add_column(new_col_name, result)
        self.dataChanged.emit()

    def perform_integral(self, operation: Callable, time_col: str, col1: str) -> None:
        """Выполнение операции интеграла"""
        result = operation(self._data, time_col, col1)
        new_col_name = f"$Integral({col1})$"
        self.add_column(new_col_name, result)
        self.dataChanged.emit()

    def show_context_menu(self, pos: QtCore.QPoint, header_index: int) -> None:
        """Показать контекстное меню для столбца"""
        current_column = self._data.columns[header_index]
        # Отключаем сигналы перед настройкой
        self.add_action.triggered.disconnect()
        self.subtract_action.triggered.disconnect()
        self.integral_action.triggered.disconnect()
        self.add_constant_action.triggered.disconnect()
        self.subtract_constant_action.triggered.disconnect()
        self.multiply_constant_action.triggered.disconnect()
        self.divide_constant_action.triggered.disconnect()
        self.hor_line_action.triggered.disconnect()
        # Настройка действий
        self.add_action.triggered.connect(
            lambda: self._handle_binary_operation(
                self._operations.add_columns, current_column
            )
        )
        self.subtract_action.triggered.connect(
            lambda: self._handle_binary_operation(
                self._operations.subtract_columns, current_column
            )
        )
        self.integral_action.triggered.connect(
            lambda: self._handle_integral_operation(
                self._operations.integral, current_column
            )
        )
        self.add_constant_action.triggered.connect(
            lambda: self._handle_constant_operation(
                self._operations.add_constant, current_column
            )
        )
        self.subtract_constant_action.triggered.connect(
            lambda: self._handle_constant_operation(
                self._operations.subtract_constant, current_column
            )
        )
        self.multiply_constant_action.triggered.connect(
            lambda: self._handle_constant_operation(
                self._operations.multiply_constant, current_column
            )
        )
        self.divide_constant_action.triggered.connect(
            lambda: self._handle_constant_operation(
                self._operations.divide_constant, current_column
            )
        )
        self.hor_line_action.triggered.connect(
            lambda: self._handle_horizontal_operation(self._operations.horizontal)
        )
        # Показываем меню
        self.context_menu.exec_(pos)

    def _handle_binary_operation(self, operation: Callable, col1: str) -> None:
        """Обработка бинарной операции"""
        columns = list(self._data.columns)
        col2, ok = QInputDialog.getItem(
            None,
            "Выбор столбца",
            "Выбран столбец: " + col1 + "\nВыберите второй столбец:",
            columns,
            0,
            False,
        )
        if ok and col2:
            self.perform_operation(operation, col1, col2)

    def _handle_integral_operation(self, operation: Callable, col1: str) -> None:
        """Обработка операции интеграла"""
        time_col = self._data.columns[0]
        reply = QMessageBox.question(
            None,
            "Подтверждение",
            f"Вычислить интеграл для столбца '{col1}'?\nВремя будет взято из столбца '{time_col}'",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes,
        )
        if reply == QMessageBox.Yes:
            self.perform_integral(operation, time_col, col1)

    def _handle_constant_operation(self, operation: Callable, col1: str) -> None:
        """Обработка операции с константой"""
        constant, ok = QInputDialog.getDouble(
            None,
            "Ввод константы",
            f"Введите константу для столбца '{col1}':",
            value=0,
            decimals=10,
        )
        if ok:
            try:
                constant = np.float64(constant)
                self.perform_constant_operation(operation, col1, constant)
            except ValueError:
                QMessageBox.warning(None, "Ошибка", "Некорректный ввод константы")
                logger.error(f"Некорректный ввод константы: {constant}")

    def _handle_horizontal_operation(self, operation: Callable) -> None:
        """Обработка операции с горизонтальной линией"""
        constant, ok = QInputDialog.getDouble(
            None,
            "Ввод константы",
            f"Введите константу:",
            value=0,
            decimals=10,
        )
        if ok:
            try:
                constant = np.float64(constant)
                self.perform_horizontal(operation, constant)
            except ValueError:
                QMessageBox.warning(None, "Ошибка", "Некорректный ввод константы")
                logger.error(f"Некорректный ввод константы: {constant}")

    def rowCount(self, parent: Optional[Any] = None) -> int:
        """Возвращает количество строк в таблице"""
        return self._data.shape[0]

    def columnCount(self, parent: Optional[Any] = None) -> int:
        """Возвращает количество столбцов в таблице"""
        return self._data.shape[1]

    def data(self, index: Any, role: int = Qt.DisplayRole) -> Optional[str]:
        """Возвращает данные для отображения в ячейке"""
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(
        self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole
    ) -> Optional[str]:
        if orientation == Qt.Horizontal:
            header_text = str(self._data.columns[section])
            if role == Qt.DisplayRole:
                return str(header_text)
            elif role == Qt.ToolTipRole:
                tooltip = f"{header_text}\nНомер: {section + 1}"
                return tooltip
        elif orientation == Qt.Vertical:
            if role == Qt.DisplayRole:
                return str(self._data.index[section])

        return None

    def get_data(self) -> pd.DataFrame:
        """Получить DataFrame с данными"""
        return self._data


class DataTableView(QTableView):
    """
    Виджет таблицы
    """

    dataChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._data_changed = False  # Флаг изменений
        self._init_ui()
        self.parent = parent

    def _init_ui(self) -> None:
        """Инициализация UI"""
        self.setWindowTitle("Таблица данных")
        self.setWindowFlags(Qt.Window)
        self.resize(800, 600)
        # Настройка заголовков
        header = self.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        header.setMinimumHeight(50)
        header.setSectionResizeMode(QHeaderView.Interactive)
        header.setStretchLastSection(True)
        header.setVisible(True)
        header.setDefaultSectionSize(250)
        header.setWhatsThis("Таблица данных")
        self.verticalHeader().setVisible(True)
        # Настройка выделения
        self.setSelectionBehavior(QTableView.SelectRows)
        self.setSelectionMode(QTableView.SingleSelection)
        # Настройка контекстного меню
        self.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        self.horizontalHeader().customContextMenuRequested.connect(
            self._show_header_menu
        )

    def set_data(self, data: pd.DataFrame) -> None:
        """Установить данные для отображения"""
        self._original_data = data.copy(deep=True)
        self.model = DataModel(self._original_data.copy())
        self.setModel(self.model)
        self._data_changed = False
        self.model.dataChanged.connect(self._on_data_changed)
        self.model.dataChanged.connect(self.dataChanged.emit)

    def _show_header_menu(self, pos) -> None:
        """Показать контекстное меню заголовка"""
        # Получаем индекс столбца под курсором
        header = self.horizontalHeader()
        index = header.logicalIndexAt(pos)
        global_pos = header.mapToGlobal(pos)
        self.model.show_context_menu(global_pos, index)

    def get_data(self) -> pd.DataFrame:
        """Получить текущие данные"""
        return self.model.get_data() if hasattr(self, "model") else None

    def _on_data_changed(self):
        """Обработчик изменения данных"""
        self._data_changed = True

    def closeEvent(self, event):
        """Перехватываем закрытие окна"""
        if self._data_changed:
            reply = QMessageBox.question(
                self,
                "Подтверждение",
                "Сохранить изменения в основном окне?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                QMessageBox.Save,
            )
            if reply == QMessageBox.Save:
                # Передаем данные в главное окно
                current_data = self.get_data()
                new_columns = list(
                    set(current_data.columns) - set(self._original_data.columns)
                )
                if new_columns:
                    # Добавляем только новые столбцы к оригинальным данным
                    for col in new_columns:
                        self.parent.data[col] = current_data[col]
                last_index = len(self.parent.data.columns)
                # Обновляем все страницы с комбобоксами и графиками
                for page in self.parent.pages:
                    for combo in page["left"].combos:
                        combo.blockSignals(True)
                        combo.insertItems(last_index, new_columns)
                        combo.blockSignals(False)
                    page["right"].data = self.parent.data
                self.parent.update_graph()
                event.accept()
            elif reply == QMessageBox.Discard:
                self.parent.data = self._original_data
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
