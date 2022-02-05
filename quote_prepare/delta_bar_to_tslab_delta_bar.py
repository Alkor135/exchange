"""
Преобразует файлы под формат TsLab
"""
import re
from datetime import datetime
from pathlib import *

import pandas as pd


def zero_hour(cell):
    """ Функция преобразует время (с финама приходят часы без нулей (с декабря 2021), которые pandas не воспринимает)"""
    cell = f'{int(cell)}'
    tmp_time = datetime.strptime(cell, "%H%M%S")
    return tmp_time.strftime("%H%M%S")


def run(source_dir_tick, target_dir):
    # Создание списка путей к дельта файлам
    delta_files: list[Path] = list(source_dir_tick.glob('*.csv'))

    for file in delta_files:

        list_split = re.split('_', file.name, maxsplit=0)  # Разделение имени файла по '_'
        tiker = list_split[0]  # Получение тикера из имени файла
        date_quote_file = re.findall(r'\d+', str(file))  # Получение цифр из пути к файлу
        target_name = f'{tiker}_delta_TS_{date_quote_file[0]}.txt'  # Создание имени новому файлу

        if Path.is_file(target_dir / target_name):
            print(f'Файл уже существует {Path(target_dir / target_name)}')
            continue
        else:
            df: pd = pd.read_csv(file, delimiter=',')  # Считываем дельта данные в DF

            # Преобразуем столбец <TIME>, где нужно добавив 0 перед часом
            df['<TIME>'] = df.apply(lambda x: zero_hour(x['<TIME>']), axis=1)

            df['<PER>'] = 1  # Создаем новый столбец <PER>, типа период
            # Перемещаем колонку на 1 место
            cols = df.columns.tolist()
            n = int(cols.index('<PER>'))
            cols = [cols[n]] + cols[:n] + cols[n + 1:]
            df = df[cols]

            df['<TICKER>'] = tiker  # Создаем новый столбец <TICKER>
            # Перемещаем колонку на 1 место
            cols = df.columns.tolist()
            n = int(cols.index('<TICKER>'))
            cols = [cols[n]] + cols[:n] + cols[n + 1:]
            df = df[cols]

            df.drop(labels=['<DELTA>'], axis=1, inplace=True)  # Удаляем ненужную колонку
            print(df)

            df.to_csv(Path(target_dir / target_name), index=False)  # Запись в файл для одного файла


if __name__ == "__main__":
    ticker: str = 'RTS'
    source_dir_tick: Path = Path(f'c:/data_quote/data_prepare_{ticker}_delta')
    target_dir: Path = Path(f'c:/data_quote/data_prepare_{ticker}_delta_TS')

    run(source_dir_tick, target_dir)
