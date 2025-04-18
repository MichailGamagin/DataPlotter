from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from src.utils.logger import Logger

logger = Logger.get_logger(__name__)

class MyNavigationToolbar(NavigationToolbar):
    """Кастомный тулбар для графика Matplotlib"""
    toolitems = (
        ("Домой", "Вернуться к исходному виду", "home", "my_home"),
        (
            "Панорамирование",
            "Перемещение осей левой кнопкой, масштабирование правой",
            "move",
            "pan",
        ),
        ("Масштаб", "Масштабировать прямоугольником", "zoom_to_rect", "zoom"),
    )
    def __init__(self, canvas, parent, plot_area, coordinates=True):
        logger.info('Инициализация MyNavigationToolbar')
        self.plot_area = plot_area
        self.view_history = {}
        self.canvas = canvas
        super().__init__(canvas, parent, coordinates)
        logger.info('Инициализация MyNavigationToolbar успешно завершена')

    def my_home(self):
        """Обработчик нажатия на кнопку Домой"""
        params = self.plot_area.get_current_params()
        time = self.plot_area.data.columns[0]
        key = tuple(params)
        ax = self.canvas.ax
        if key in self.view_history:
            xlim, ylim = self.view_history[key]
            ax.set_xlim(xlim)
            ax.set_ylim(ylim)
        else:
            if time in self.plot_area.data.columns:
                x_axis_limit = self.plot_area.data[time].max()
                ax.set_xlim(0, x_axis_limit)
            else:
                ax.set_xlim(0, 1000)
            y_min, y_max = ax.get_ylim()
            ax.set_ylim(y_min, y_max)
        self.canvas.draw()

    def save_current_view(self):
        """
        Сохраняет текущий вид графика для выбранных параметров.
        """
        # Получаем текущие выбранные параметры.
        params = self.plot_area.get_current_params()
        key = tuple(params)
        # Сохраняем пределы по осям x и y.
        xlim = self.canvas.ax.get_xlim()
        ylim = self.canvas.ax.get_ylim()

        self.view_history[key] = (xlim, ylim)