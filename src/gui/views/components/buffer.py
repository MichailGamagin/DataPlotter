"""Модуль содержит буфер обмена для копирования и вставки данных с графиков"""

class Buffer:
    def __init__(self) -> None:
        self.buffer = {
            "lists": [],
            "Y_axis": {
                "group": None,
                "limits": None,
                "sizing": None,
            },
            "X_axis": {
                "group": None,
                "limits": None,
                "sizing": None,
            },
            "marker_freq": None,
            "line_spacing": None,
            "alternative_caption": None,
        }

    def copy(self, page_data: dict, alt_caption: str):
        self.buffer["lists"] = [
            combobox.currentText() for combobox in page_data["left"].combos
        ]
        self.buffer["Y_axis"]["group"] = page_data["right"].group.currentText()
        self.buffer["Y_axis"]["limits"] = page_data["right"].y_settings.text()
        self.buffer["Y_axis"]["sizing"] = page_data["right"].sizing_cmb.currentText()
        self.buffer["X_axis"]["group"] = page_data["right"].group_x.currentText()
        self.buffer["X_axis"]["limits"] = page_data["right"].x_settings.currentText()
        self.buffer["X_axis"]["sizing"] = page_data["right"].sizing_cmb_x.currentText()
        self.buffer["marker_freq"] = page_data["right"].markers.currentText()
        self.buffer["line_spacing"] = page_data["right"].x_spacing_grid_spinBox.value()
        self.buffer["alternative_caption"] = alt_caption

    def paste(self):
        left: list = self.buffer["lists"]
        right: dict = {key: self.buffer[key] for key in list(self.buffer.keys())[1:-1]}
        return left, right, self.buffer["alternative_caption"]
