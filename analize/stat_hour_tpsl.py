"""
Скрипт собирает статистику по файлам ТПСЛ
"""
import re
from pathlib import *
from datetime import datetime

import pandas as pd

# Настройки отображения DF
pd.set_option('max_rows', 5)  # Установка 5 строк вывода DF
pd.set_option('display.max_columns', None)  # Сброс ограничений на число столбцов


def zero_hour(cell):
    """ Функция преобразует время (с финама приходят часы без нулей (с марта 2021), которые pandas не воспринимает)"""
    cell = f'{int(cell)}'
    tmp_time = datetime.strptime(cell, "%H%M%S")
    return tmp_time.strftime("%H%M%S")


def dataframe_datetime_prepare(df: pd):
    df['<TIME>'] = df.apply(lambda x: zero_hour(x['<TIME>']),
                            axis=1)  # Преобразуем столбец <TIME>, где нужно добавив 0 перед часом
    df['<DATE_TIME>'] = df['<DATE>'].astype(str) + ' ' + df['<TIME>'].astype(
        str)  # Создаем новый столбец <DATE_TIME> слиянием столбцов <DATE> и <TIME>
    df = df.set_index(pd.DatetimeIndex(df['<DATE_TIME>']))  # Меняем индекс и делаем его типом datetime
    df.drop(labels=['<DATE_TIME>', '<DATE>', '<TIME>', '<VOL>'], axis=1,
            inplace=True)  # Удаляем ненужные колонки. axis=1 означает, что отбрасываем колонку а не индекс
    return df


def run(files_path, razmer, year):
    result: pd = pd.DataFrame()
    for ind_file, file in enumerate(files_path, start=1):  # Итерация по тиковым файлам
        df = pd.read_csv(file, delimiter=',')  # Считываем данные в DF
        df = dataframe_datetime_prepare(df)
        # print(df)
        for row in df.itertuples():
            if row[0].hour in result.columns:
                print('first')
                if row[7] == 3:
                    print('second')
                    result.loc[0, row[0].hour] = 1
            else:
                # result.insert(0, row[0].hour, 0)
                result[row[0].hour] = 0

            # print(row[0])
            # print(row[0].hour)
            # tmp_time = datetime.strftime(row[0], "%Y-%m-%d %H:%M:%S")
            # print(tmp_time)
            # # print(datetime.strptime(row[2]))
            # # print(row[2])
            # break

        break
    print(result)


if __name__ == "__main__":
    razmer: int = 250
    ticker: str = 'RTS'
    year: str = '2022'

    source_dir: Path = Path(f'c:\data_quote\data_prepare_{ticker}_range_mvc_tpsl')  # Путь к ресурсному каталогу

    # Создание списка путей к файлам
    files_path: list[Path] = list(source_dir.glob(f'*{razmer}*{year}*.txt'))

    run(files_path, razmer, year)
