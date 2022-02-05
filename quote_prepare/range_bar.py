"""
Скрипт из файлов с тиковыми данными делает файл с рандже барами
"""
import re
from pathlib import *

import pandas as pd


def run(tick_files: list[Path], razmer: int, target_dir: Path):

    for ind_file, tick_file in enumerate(tick_files):  # Итерация по тиковым файлам

        list_split = re.split('_', tick_file.name, maxsplit=0)  # Разделение имени файла по '_'
        tiker = list_split[0]  # Получение тикера из имени файла
        date_quote_file = re.findall(r'\d+', str(tick_file))  # Получение цифр из пути к файлу
        target_name = f'{tiker}_delta_{date_quote_file[0]}.csv'  # Создание имени новому файлу

        if Path.is_file(target_dir / target_name):
            print(f'Файл уже существует {Path(target_dir / target_name)}')
            continue
        else:
            df_ticks_file: pd = pd.read_csv(tick_file, delimiter=',')  # Считываем тиковые данные в DF
            # previous_tick = 0
            # direction_tick_up = True

            # Создание DF под рандже бары одного тикового файла
            df: pd = pd.DataFrame(columns='<DATE> <TIME> <OPEN> <HIGH> <LOW> <CLOSE> <VOL>'.split(' '))

            for tick in df_ticks_file.itertuples():  # Итерация по строкам тикового DF
                # print(f'{tick[1]} {tick[2]}')
                print('\rCompleted file: {:.2f}%. Completed files: {:.2f}%'.format(
                    tick[0] * 100 / len(df_ticks_file.index),
                    ind_file * 100 / len(tick_files)
                    ),
                    end=''
                )


if __name__ == "__main__":
    razmer: int = 150
    ticker: str = 'RTS'
    year_tick: str = '2022'

    source_dir_tick: Path = Path(f'c:/data_quote/data_finam_{ticker}_tick')  # Путь к ресурсному каталогу
    target_dir: Path = Path(f'c:/data_quote/data_prepare_{ticker}_range')  # Путь к целевому каталогу

    # Создание списка путей к файлам с тиками
    tick_files: list[Path] = list(source_dir_tick.glob(f'*{year_tick}*.csv'))

    run(tick_files, razmer, target_dir)
