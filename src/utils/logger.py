import logging
from pathlib import Path
from datetime import datetime


class Logger:
    """Класс для настройки и управления логгированием"""

    def __init__(self):
        self.logs_dir = Path(__file__).resolve().parent.parent.parent / 'logs'
        self.logs_dir.mkdir(parents=True, exist_ok=True)  
        
        self.log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        self.date_format = '%Y-%m-%d_%H-%M-%S'

        current_date = datetime.now().strftime('%Y-%m-%d')
        self.log_file = self.logs_dir / f'app_{current_date}.log'

        logging.basicConfig(
            level=logging.INFO,
            format=self.log_format,
            datefmt=self.date_format,
            handlers=[
                logging.FileHandler(self.log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
    @staticmethod
    def get_logger(name) -> logging.Logger:
        """Получить логгер для конкретного модуля"""
        return logging.getLogger(name)
    