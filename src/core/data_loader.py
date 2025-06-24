"""
В этом файле содержатся функции распаковки выходных данных из теплогидравлических кодов и некоторые вспомогательные функции.
Описание функций приведено в функциях.
"""
from pathlib import Path
from struct import unpack
from collections import Counter

import pandas as pd
import numpy as np

from src.core.constants import BASE_DIR, DEFAULT_FILE_PATH
from src.utils.logger import Logger

logger = Logger.get_logger(__name__)


class DataLoader:

    default_data: pd.DataFrame = pd.DataFrame(data = {
        "Время, с": np.arange(100),
        "Параметр, кг": np.arange(100),
    })
    
    def __init__(self, path: str | Path, enc: str) -> None:
        if Path(path).exists():
            self.path: Path = Path(path).resolve()
        else:
            raise FileNotFoundError
        self.encoding: str = enc
        self.data: pd.DataFrame = self.default_data
        self.set_data()
        dublicate = self.find_dublicates(self.data.columns.to_list())
        if dublicate:
            raise DublicatedColumnsError(dublicate)

    def find_dublicates(self, string_list: list[str]):
        """Функция нахождения дубликатов параметров"""
        counts = Counter(string_list)
        dublicates = [s for s, count in counts.items() if count > 1]
        return dublicates
    
    def get_data(self) -> pd.DataFrame:
        return self.data

    def set_data(self):
        """
        Загружает данные из разных источников (KORSAR, TRAP(csv, lent3)).
        """
        logger.info(f"Загрузка данных из файла: {self.path}")
        try:
            # Try KORSAR (text format)
            self.data = self.data_KORSAR()
            if self.data is not None:
                logger.info(f"Данные успешно загружены из файла: {self.path}")

            # Try TRAP (CSV format)
            self.data = self.data_TRAP_csv()
            if self.data is not None:
                logger.info(f"Данные успешно загружены из файла: {self.path}")

            # Try LENT
            self.data = self.read_TRAP_lent()
            if self.data is not None:
                logger.info(f"Данные успешно загружены из файла: {self.path}")
            ###
            # Тут можно вставить свою функцию для чтения нужного формата
            ###
            if self.data is None:
                self.data = self.default_data

        except Exception as e:
            logger.info(
                f"Неожиданная ошибка при загрузке данных из файла: {self.path}:\n {e}"
            )
            self.data = self.default_data

    def data_KORSAR(self) -> pd.DataFrame | None:
        """
        Считывает данные из файла формата KORSAR."""
        try:
            with open(self.path, "r", encoding=self.encoding) as dat:
                length = int(dat.readline().strip())
                headers = [next(dat).strip().replace("\n", "") for _ in range(length)]
            data = np.loadtxt(
                self.path, encoding=self.encoding, dtype=float, skiprows=length + 1
            )
            df = pd.DataFrame(data, columns=headers)
            return df
        except Exception as e:
            return None

    def data_TRAP_csv(self) -> pd.DataFrame | None:
        """
        Считывает данные из выходного файла Korr_v49 в формате csv."""
        # Количество параметров по умолчанию в ТРАПе(первые 24 в lent3)
        count_default_TRAP_params = 24
        try:
            csv = pd.read_csv(
                self.path, encoding="windows-1251", header=2, sep=";", dtype="float64"
            )
            col = [header.strip() for header in csv.columns.to_list()]
            col_new = [
                replace_eng_with_rus(name) if idx < count_default_TRAP_params else name
                for idx, name in enumerate(col)
            ]
            df = pd.read_csv(
                self.path,
                encoding="windows-1251",
                header=2,
                sep=";",
                dtype="float64",
                names=col_new,
            )
            return df
        except Exception as e:
            return None

    def read_TRAP_lent(self) -> pd.DataFrame | None:
        """ Считывает данные из файла формата LENT."""
        # Количество параметров по умолчанию в ТРАПе(первые 24 в lent3)
        count_default_TRAP_params = 24
        try:
            with open(self.path, "rb") as f:
                # Пропускаем первые 4 байта
                f.seek(4)
                # Считываем количество параметров
                N = int.from_bytes(f.read(4), "little")
                # Пропускаем следующие 4 байта
                f.seek(4, 1)
                # Пропускаем N+1 блоков по 4 байта
                f.seek(4 * (N + 1), 1)

                # Считываем названия параметров
                names = [f.read(60).decode("cp866").strip() for _ in range(N)]
                names_new = [
                    (
                        replace_eng_with_rus(name)
                        if idx < count_default_TRAP_params
                        else name
                    )
                    for idx, name in enumerate(names)
                ]
                data_list = []
                time_list = []
                while True:
                    # Пропускаем 8 байт
                    f.seek(8, 1)
                    # Считываем время (4 байта)
                    btau = f.read(4)
                    tau = unpack("f", btau)[0]
                    time_list.append(tau)
                    # Проверяем условие остановки (дублирование времени)
                    if len(time_list) >= 2 and time_list[-1] == time_list[-2]:
                        time_list.pop()
                        break
                    # Считываем данные параметров (N-1 параметров по 4 байта)
                    row_data = [unpack("f", f.read(4))[0] for _ in range(N - 1)]
                    data_list.append(row_data)

                time_array = np.array(time_list)
                data_array = np.array(data_list)

                df = pd.DataFrame(data_array, columns=names_new[1:])
                df.insert(0, "Время, с", time_array)
                return df
        except Exception as e:
            return None

def replace_eng_with_rus(text: str) -> str:
    "Функция приведения символов в строке из смеси английских и русских букв к строке с только русскими буквами"
    eng_to_rus = {
        "A": "А",
        "B": "В",
        "C": "С",
        "E": "Е",
        "H": "Н",
        "K": "К",
        "M": "М",
        "O": "О",
        "P": "Р",
        "T": "Т",
        "X": "Х",
        "Y": "У",
    }
    result = ""
    for char in text:
        if char.upper() in eng_to_rus:
            result += eng_to_rus[char.upper()]
        else:
            result += char
    return result

class DublicatedColumnsError(Exception):
    """Класс исключений при дублировании столбцов в DataFrame"""
    def __init__(self, dublicated_columns: list = None) -> None:
        if dublicated_columns is None:
            self.dublicated_columns = []
        else:
            self.dublicated_columns = dublicated_columns
        super().__init__(
            f"Набор данных содержит дубликаты параметров: {self.dublicated_columns}"
        )


if __name__ == "__main__":

    path_TRAP = BASE_DIR / "data" + "\\test.csv"
    path_KORSAR = BASE_DIR / "data" + "\\res_cyclic.txt"
    path_lent = BASE_DIR / "data" + "\\lent3"
    data = load_data_from(path_lent, enc="cp1251")
    # data = read_lent(path_lent)
    print(data)
