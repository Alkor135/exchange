"""
Скрипт берет файлы с рендж барами и файлы с тиками рассчитывает максимальный объем в кластере
"""
import re
from datetime import datetime
from pathlib import *

import pandas as pd


def run(tick_files: list[Path], range_files: list[Path], razmer: int, target_dir: Path):
    for ind_r, range_file in enumerate(range_files, start=1):  # Итерация по range файлам
        df: pd = pd.read_csv(range_file, delimiter=',')  # Загрузка в DF range файла
        df['<MAX_VOLUME_PRICE>'] = None  # Создание новой колонки
        df['<MAX_VOLUME_CLUSTER>'] = None  # Создание новой колонки
        pattern_re = r'_\d+'
        poisk = re.search(pattern_re, str(range_file))
        print(poisk)
        break


if __name__ == "__main__":
    razmer: int = 150
    ticker: str = 'RTS'
    year_tick: str = '2022'

    source_dir_tick: Path = Path(f'c:/data_quote/data_finam_{ticker}_tick')  # Путь к ресурсному каталогу с тиками
    source_dir_range: Path = Path(f'c:/data_quote/data_prepare_{ticker}_range')  # Путь к ресурсному каталогу с range
    target_dir: Path = Path(f'c:/data_quote/data_prepare_{ticker}_range_max_vol')  # Путь к целевому каталогу

    if not target_dir.is_dir(): target_dir.mkdir()  # Создание каталога

    tick_files: list[Path] = list(source_dir_tick.glob(f'*{year_tick}*.csv'))  # Создание списка путей к файлам с тиками
    range_files: list[Path] = list(source_dir_range.glob(f'*{year_tick}*.txt'))  # Создание списка путей к файлам с range
    range_files = [x for x in range_files if f'{razmer}' in str(x)]  # Фильтрация списка по размеру ренджа

    run(tick_files, range_files, razmer, target_dir)
