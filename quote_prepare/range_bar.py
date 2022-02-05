"""
Скрипт из файлов с тиковыми данными делает файл с дельта барами
"""
import re
from pathlib import *

import pandas as pd



if __name__ == "__main__":
    ticker: str = 'RTS'
    year_tick: str = '2022'
    delta_max_val: int = 500
    source_dir_tick: Path = Path(f'c:/data_quote/data_finam_{ticker}_tick')  # Путь к ресурсному каталогу
    target_dir: Path = Path(f'c:/data_quote/data_prepare_{ticker}_delta')  # Путь к целевому каталогу

    # Создание списка путей к файлам с тиками
    tick_files: list[Path] = list(source_dir_tick.glob(f'*{year_tick}*.csv'))

    run(tick_files, delta_max_val, target_dir)