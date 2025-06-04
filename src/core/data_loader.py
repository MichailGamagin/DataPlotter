"""
В этом файле содержатся функции распаковки выходных данных из теплогидравлических кодов и некоторые вспомогательные функции.
Описание функций приведено в функциях.
"""
from struct import unpack
from collections import Counter
import pandas as pd
import numpy as np

from src.core.constants import BASE_DIR, DEFAULT_FILE_PATH
from src.utils.logger import Logger

logger = Logger.get_logger(__name__)


def data_KORSAR(path: str, enc: str) -> pd.DataFrame:
    """
    Считывает данные из файла формата KORSAR.

    Args:
        path (str): Путь к файлу.
        enc (str): Кодировка файла.

    Returns:
        pd.DataFrame: DataFrame с данными.
    """
    try:
        with open(path, "r", encoding=enc) as dat:
            length = int(dat.readline().strip())
            headers = [next(dat).strip().replace("\n", "") for _ in range(length)]
        data = np.loadtxt(path, encoding=enc, dtype=float, skiprows=length + 1)
        df = pd.DataFrame(data, columns=headers)
        # return numeric_columns(df)
        return df
    except Exception as e:
        return None


def data_TRAP_csv(path: str) -> pd.DataFrame | None:
    """
    Считывает данные из выходного файла Korr_v49 в формате csv.

    Args:
        path (str): Путь к файлу.

    Returns:
        pd.DataFrame: DataFrame с данными.
    """
    # Количество параметров по умолчанию в ТРАПе(первые 24 в lent3)
    count_default_TRAP_params = 24
    try:
        csv = pd.read_csv(
            path, encoding="windows-1251", header=2, sep=";", dtype="float64"
        )
        col = [header.strip() for header in csv.columns.to_list()]
        col_new = [
            replace_eng_with_rus(name) if idx < count_default_TRAP_params else name
            for idx, name in enumerate(col)
        ]
        dublicates = find_dublicates(col_new)
        if dublicates:
            logger.error(f"Набор данных содержит дубликаты параметров: {dublicates}")
            return f"Набор данных содержит дубликаты параметров:\n{dublicates}"
        df = pd.read_csv(
            path,
            encoding="windows-1251",
            header=2,
            sep=";",
            dtype="float64",
            names=col_new,
        )
        # return numeric_columns(df)
        return df
    except Exception as e:
        return None


def read_TRAP_lent(path) -> pd.DataFrame | None:
    """
    Считывает данные из файла формата LENT.

    Args:
        path (str): Путь к файлу LENT.

    Returns:
        - df (pd.DataFrame): DataFrame с данными, где первый столбец - время, остальные - параметры.
    """
    # Количество параметров по умолчанию в ТРАПе(первые 24 в lent3)
    count_default_TRAP_params = 24
    try:
        with open(path, "rb") as f:
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
                replace_eng_with_rus(name) if idx < count_default_TRAP_params else name
                for idx, name in enumerate(names)
            ]
            dublicates = find_dublicates(names_new)
            if dublicates:
                logger.error(f"Набор данных содержит дубликаты параметров: {dublicates}")
                return f"Набор данных содержит дубликаты параметров:\n{dublicates}"
            # Считываем данные и время
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

            # Преобразуем списки в NumPy массивы
            time_array = np.array(time_list)
            data_array = np.array(data_list)

            # Создаем DataFrame
            df = pd.DataFrame(data_array, columns=names_new[1:])
            df.insert(0, "Время, с", time_array)
            return df
            # return numeric_columns(df)

    except Exception as e:
        return None


def load_data_from(path: str, enc: str):
    """
    Загружает данные из разных источников (KORSAR, TRAP(csv, lent3)).

    Args:
        path (str): Путь к файлу.
        enc (str): Кодировка файла.

    Returns:
        pd.DataFrame: DataFrame с данными.
    """
    logger.info(f"Загрузка данных из файла: {path}")
    if not path:
        return pd.DataFrame(
            data={"Время, с": np.arange(100), "Параметр, кг": np.arange(100)}
        )

    try:
        # Try KORSAR (text format)
        data = data_KORSAR(path, enc)
        if data is not None:
            logger.info(f"Данные успешно загружены из файла: {path}")
            return data

        # Try TRAP (CSV format)
        data = data_TRAP_csv(path)
        if data is not None:
            logger.info(f"Данные успешно загружены из файла: {path}")
            return data

        # Try LENT
        data = read_TRAP_lent(path)
        if data is not None:
            logger.info(f"Данные успешно загружены из файла: {path}")
            return data

        logger.info(
            f"Не удалось загрузить данные из файла: {path}\n"
            "Возвращен дефолтный DataFrame."
        )
        return pd.DataFrame(
            data={"Время, с": np.arange(100), "Параметр, кг": np.arange(100)}
        )

    except FileNotFoundError:
        logger.info(f"Файл не найден: {path}")
        return pd.DataFrame(
            data={"Время, с": np.arange(100), "Параметр, кг": np.arange(100)}
        )
    except Exception as e:
        logger.info(f"Неожиданная ошибка при загрузке данных из файла: {path}:\n {e}")
        return pd.DataFrame(
            data={"Время, с": np.arange(100), "Параметр, кг": np.arange(100)}
        )


def numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Добавление нумерации в названия столбцов DataFrame"""
    new_df = df.copy(deep=True)
    new_columns = {col: f"{i}. {col}" for i, col in enumerate(df.columns)}
    new_df.rename(columns=new_columns, inplace=True)
    return new_df


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

def  find_dublicates(string_list):
    """Функция нахождения дубликатов параметров"""
    counts = Counter(string_list)
    dublicates = [s for s, count in counts.items() if count > 1]
    return dublicates

if __name__ == "__main__":

    path_TRAP = BASE_DIR / "data" + "\\test.csv"
    path_KORSAR = BASE_DIR / "data" + "\\res_cyclic.txt"
    path_lent = BASE_DIR / "data" + "\\lent3"
    data = load_data_from(path_lent, enc="cp1251")
    # data = read_lent(path_lent)
    print(data)
