"""
Скрипт исправляет время (добавляет 0 перед однозначным часом), для множества файлов
Нужно для TsLab и Pandas(построение графиков)
"""
from datetime import datetime
from pathlib import *

import pandas as pd


def zero_hour(cell):
    """ Функция преобразует время (с финама приходят часы без нулей (с декабря 2021), которые pandas не воспринимает)"""
    cell = f'{int(cell)}'
    tmp_time = datetime.strptime(cell, "%H%M%S")
    return tmp_time.strftime("%H%M%S")


if __name__ == "__main__":
    dir_path: Path = Path('c:\data_quote\data_prepare_RTS_range')  # Путь к каталогу с файлами в которых испр время

    files_lst: list[Path] = list(dir_path.glob(f'*.csv'))  # Создание списка путей к файлам

    for ind_file, file in enumerate(files_lst):

        print('\rCompleted files: {:.2f}%'.format((ind_file + 1) * 100 / len(files_lst)), end='')  # Прогресс

        df: pd = pd.read_csv(file, delimiter=',')  # Считываем тиковые данные в DF
        try:
            # Преобразуем столбец <TIME>, где нужно добавив 0 перед часом
            df['<TIME>'] = df.apply(lambda x: zero_hour(x['<TIME>']), axis=1)
        except Exception as err:
            print(err)
        else:
            file.unlink()  # Удаление файла
            df.to_csv(file, index=False)  # Запись в файл

