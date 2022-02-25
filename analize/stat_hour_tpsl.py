"""
Скрипт собирает статистику по файлам ТПСЛ
"""
from typing import Any
import re
from pathlib import *
from datetime import datetime

import pandas as pd

# Настройки отображения DF
pd.set_option('max_rows', 5)  # Установка 5 строк вывода DF
pd.set_option('display.max_columns', None)  # Сброс ограничений на число столбцов


def zero_hour(cell: Any) -> str:
    """ Функция преобразует время (с финама приходят часы без нулей (с марта 2021), которые pandas не воспринимает)"""
    cell: str = f'{int(cell)}'
    tmp_time: datetime = datetime.strptime(cell, "%H%M%S")
    return tmp_time.strftime("%H%M%S")


def dataframe_datetime_prepare(df: pd) -> pd:
    """ Функция обрабатывает столбцы с датой и временем"""
    df['<TIME>'] = df.apply(lambda x: zero_hour(x['<TIME>']),
                            axis=1)  # Преобразуем столбец <TIME>, где нужно добавив 0 перед часом
    df['<DATE_TIME>'] = df['<DATE>'].astype(str) + ' ' + df['<TIME>'].astype(
        str)  # Создаем новый столбец <DATE_TIME> слиянием столбцов <DATE> и <TIME>
    df = df.set_index(pd.DatetimeIndex(df['<DATE_TIME>']))  # Меняем индекс и делаем его типом datetime
    df.drop(labels=['<DATE_TIME>', '<DATE>', '<TIME>', '<VOL>'], axis=1,
            inplace=True)  # Удаляем ненужные колонки. axis=1 означает, что отбрасываем колонку а не индекс
    return df


def run(files_path, razmer, year):
    result_total: pd = pd.DataFrame()
    for ind_file, file in enumerate(files_path, start=1):  # Итерация по файлам
        result3: pd = pd.DataFrame()
        df = pd.read_csv(file, delimiter=',')  # Считываем данные в DF
        df = dataframe_datetime_prepare(df)

        for row in df.itertuples():  # Итерация по рандже барам
            if row[0].hour not in result3.columns:  # Если столбец с таким часом не существует
                result3[row[0].hour] = [0, 0, 0]  # Создаем столбец, заполняем нулями

            # Подсчет для ТП3
            if row[7] == 3:
                result3.loc[0, row[0].hour] += 3  #
            elif row[7] == -1 or row[7] == 1 or row[7] == 2:
                result3.loc[0, row[0].hour] -= 1

            # Подсчет для ТП2
            if row[7] == 2 or row[7] == 3:
                result3.loc[1, row[0].hour] += 2  #
            elif row[7] == -1 or row[7] == 1:
                result3.loc[1, row[0].hour] -= 1

            # Подсчет для ТП1
            if row[7] == 2 or row[7] == 3 or row[7] == 1:
                result3.loc[2, row[0].hour] += 1  #
            elif row[7] == -1:
                result3.loc[2, row[0].hour] -= 1

        if len(result_total) == 0:
            result_total = result3
        else:
            # Сложение DF
            result_total = result_total.add(result3).combine_first(result_total).combine_first(result3)

        print(file.name)
        print(result3)
        print()
    print(f'Совокупный результат')
    print(result_total)


if __name__ == "__main__":
    razmer: int = 250
    ticker: str = 'RTS'
    year: str = '2021'

    # source_dir: Path = Path(f'c:\data_quote\data_prepare_{ticker}_range_mvc_tpsl')  # Путь к ресурсному каталогу
    # print(fr'c:\Users\Alkor\gd\data_quote\data_prepare_{ticker}_range_mvc_tpsl')
    source_dir: Path = Path(fr'c:\Users\Alkor\gd\data_quote\data_prepare_{ticker}_range_mvc_tpsl')  # Путь к ресурсному каталогу

    # Создание списка путей к файлам
    files_path: list[Path] = list(source_dir.glob(f'*{razmer}*{year}*.txt'))

    run(files_path, razmer, year)
