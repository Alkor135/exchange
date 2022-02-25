"""
Скрипт исправляет время (добавляет 0 перед однозначным часом), для одного файла
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
    file_path: Path = Path('c:\data_quote\data_prepare_RTS_range_mvc_tpsl_sec\SPFB.RTS_00_range250_splice_2022.txt')  # Путь к файлу
    # file_path: Path = Path('c:\data_quote\data_prepare_RTS_range\SPFB.RTS_00_range250_splice_2022.txt')  # Путь к файлу

    df: pd = pd.read_csv(file_path, delimiter=',')  # Считываем данные в DF
    try:
        # Преобразуем столбец <TIME>, где нужно добавив 0 перед часом
        df['<TIME>'] = df.apply(lambda x: zero_hour(x['<TIME>']), axis=1)
    except Exception as err:
        print(err)
    else:
        file_path.unlink()  # Удаление файла
        df.to_csv(file_path, index=False)  # Запись в файл
