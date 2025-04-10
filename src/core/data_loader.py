from struct import unpack
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
        return pd.DataFrame(data, columns=headers)
    except Exception as e:
        return None


def data_TRAP_csv(path: str) -> pd.DataFrame | None:
    """
    Считывает данные из выходного файла TRAP в формате csv.
    
    Args:
        path (str): Путь к файлу.

    Returns:
        pd.DataFrame: DataFrame с данными.
    """
    try:
        csv = pd.read_csv(
            path, encoding="windows-1251", header=2, sep=";", dtype="float64"
        )
        col = [header.strip() for header in csv.columns.to_list()]
        return pd.read_csv(
            path,
            encoding="windows-1251",
            header=2,
            sep=";",
            dtype="float64",
            names=col,
            
        )
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
            df = pd.DataFrame(data_array, columns=names[1:])
            df.insert(0, "Время, с", time_array)
            return df
    
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
        
        
        logger.info(f"Не удалось загрузить данные из файла: {path}\n"
              "Возвращен дефолтный DataFrame.")
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


if __name__ == "__main__":
    
    path_TRAP = BASE_DIR / 'data' + "\\test.csv"
    path_KORSAR = BASE_DIR / 'data' + "\\res_cyclic.txt"
    path_lent = BASE_DIR / 'data' + "\\lent3"
    data = load_data_from(path_lent, enc="cp1251")
    # data = read_lent(path_lent)
    print(data)
