"""
Скрипт собирает статистику по одному файлу ТПСЛ
"""
import re
from pathlib import *
from datetime import datetime
from typing import Any

import pandas as pd


# Настройки отображения DF
pd.set_option('max_rows', 5)  # Установка 5 строк вывода DF
pd.set_option('display.max_columns', None)  # Сброс ограничений на число столбцов


def zero_hour(cell: Any) -> str:
    """ Функция преобразует время (с финама приходят часы без нулей (с марта 2021), которые pandas не воспринимает)"""
    cell: str = f'{int(cell)}'
    tmp_time: datetime = datetime.strptime(cell, "%H%M%S")
    return tmp_time.strftime("%H%M%S")


def dataframe_datetime_conversion(df: pd) -> pd:
    """ Функция обрабатывает столбцы с датой и временем, переводя их в формат datetime"""
    df['<TIME>'] = df.apply(lambda x: zero_hour(x['<TIME>']),
                            axis=1)  # Преобразуем столбец <TIME>, где нужно добавив 0 перед часом
    df['<DATE_TIME>'] = df['<DATE>'].astype(str) + ' ' + df['<TIME>'].astype(
        str)  # Создаем новый столбец <DATE_TIME> слиянием столбцов <DATE> и <TIME>
    df = df.set_index(pd.DatetimeIndex(df['<DATE_TIME>']))  # Меняем индекс и делаем его типом datetime
    df.drop(labels=['<DATE_TIME>', '<DATE>', '<TIME>', '<VOL>'], axis=1,
            inplace=True)  # Удаляем ненужные колонки. axis=1 означает, что отбрасываем колонку а не индекс
    return df


def run(source_file):

    df = pd.read_csv(source_file, delimiter=',')  # Считываем данные в DF

    df = df.loc[df['<TP_SL>'] != 0]  # Убираем строки где <TP_SL> равен 0 (конец дня)
    # Убираем строки где кластер с макс объемом вне бара (быстрое движение рынка)
    df = df.loc[df['<HIGH>'] > df['<MAX_VOLUME_PRICE>']]
    df = df.loc[df['<MAX_VOLUME_PRICE>'] > df['<LOW>']]

    df = dataframe_datetime_conversion(df)  # Преобразование даты и времени в форма datetime и в индекс

    result3: pd = pd.DataFrame()
    result_count: pd = pd.DataFrame()
    for row in df.itertuples():  # Итерация по рандже барам
        if row[0].hour not in result3.columns:  # Если столбец с таким часом не существует
            result3[row[0].hour] = [0, 0, 0]  # Создаем столбец, заполняем нулями
        if row[0].hour not in result_count.columns:  # Если столбец с таким часом не существует
            result_count[row[0].hour] = [0, 0, 0, 0]  # Создаем столбец, заполняем нулями

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

        if row[7] == 3:
            result_count.loc[0, row[0].hour] += 1
        elif row[7] == 2:
            result_count.loc[1, row[0].hour] += 1
        elif row[7] == 1:
            result_count.loc[2, row[0].hour] += 1
        elif row[7] == -1:
            result_count.loc[3, row[0].hour] += 1

    print('\n', source_file.name)
    print(result3)
    print(result_count)

    # print('\n', source_file.name)
    # print(df['<TP_SL>'].value_counts())
    # print(df['<TP_SL>'].value_counts(normalize=True))

    # df_counts = df['<TP_SL>'].value_counts()
    # print(type(df_counts))


if __name__ == "__main__":
    # Путь к файлу

    source_file1: Path = Path(
        fr'c:\Users\Alkor\gd\data_quote\data_prepare_RTS_range_mvc_tpsl_sec\SPFB.RTS_00_range250_splice_2021.txt')
    source_file2: Path = Path(
        fr'c:\Users\Alkor\gd\data_quote\data_prepare_RTS_range_mvc_tpsl_sec\SPFB.RTS_00_range250_splice_2022.txt')

    run(source_file1)
    run(source_file2)
