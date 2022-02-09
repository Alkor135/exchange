"""
Скрипт склеивает файлы.
Объединяет DataFrame
"""
import re
from pathlib import *

import pandas as pd


def run(files: list[Path], razmer: int, year: str, target_dir: Path) -> None:
    result: pd = pd.DataFrame()
    tiker: str = ''
    for ind_file, file in enumerate(files, start=1):  # Итерация по тиковым файлам
        print('\rCompleted files: {:.2f}%'.format(ind_file * 100 / len(files)), end='')  # Прогресс

        # Парсинг имени файла
        list_split = re.split('_', file.name, maxsplit=0)  # Разделение имени файла по '_'
        tiker = list_split[0]  # Получение тикера из имени файла

        df = pd.read_csv(file, delimiter=',')  # Считываем данные в DF
        result = result.append(df)

    target_name: str = f'{tiker}_00_range{razmer}_splice_{year}.txt'  # Создание имени новому файлу
    target_file: Path = Path(target_dir / target_name)  # Составление пути к новому файлу
    result.to_csv(target_file, index=False)  # Запись в файл


if __name__ == "__main__":
    razmer: int = 250
    ticker: str = 'RTS'
    year: str = '2021'

    # source_dir_tick: Path = Path(f'c:/data_quote/data_prepare_{ticker}_range')  # Путь к ресурсному каталогу
    source_dir_tick: Path = Path(f'c:\data_quote\data_prepare_{ticker}_range_max_vol')  # Путь к ресурсному каталогу
    target_dir: Path = Path(f'c:\data_quote\data_prepare_{ticker}_range_max_vol')  # Путь к целевому каталогу

    # Создание списка путей к файлам с тиками
    files_path: list[Path] = list(source_dir_tick.glob(f'*{razmer}*{year}*.txt'))

    run(files_path, razmer, year, target_dir)
