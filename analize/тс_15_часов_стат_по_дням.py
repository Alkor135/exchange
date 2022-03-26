"""
Скрипт торговой системы входа в 15 часов нв возврат(разворот)
"""
from typing import Any
from pathlib import *
from datetime import datetime, timezone

import pandas as pd


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
    df.drop(labels=['<DATE_TIME>', '<DATE>', '<TIME>'], axis=1,
            inplace=True)  # Удаляем ненужные колонки. axis=1 означает, что отбрасываем колонку а не индекс
    return df


def clearing_df(df: pd):
    """Функция очистки DF"""
    df = df.loc[df['<TP_SL>'] != 0]  # Убираем строки где <TP_SL> равен 0 (конец дня)
    # Убираем строки где кластер с макс объемом вне бара (быстрое движение рынка)
    df = df.loc[df['<HIGH>'] > df['<MAX_VOLUME_PRICE>']]
    df = df.loc[df['<MAX_VOLUME_PRICE>'] > df['<LOW>']]
    df.drop(labels=['<OPEN>',
                    '<HIGH>',
                    '<LOW>',
                    '<CLOSE>',
                    '<MAX_VOLUME_PRICE>',
                    '<MAX_VOLUME_CLUSTER>',
                    '<VOL>'], axis=1, inplace=True)
    return df


def tp_3(cell: Any):
    """ Функция преобразует время (с финама приходят часы без нулей (с марта 2021), которые pandas не воспринимает)"""
    if cell < 3:
        return -1
    return cell


def run(file_path):
    # Загружаем файл в DF
    df = pd.read_csv(file_path, delimiter=',')
    df = dataframe_datetime_conversion(df)
    df = clearing_df(df)
    # print(df)
    df = df.loc[df.index.hour == 15]
    df['<TP_SL>'] = df.apply(lambda x: tp_3(x['<TP_SL>']), axis=1)
    # print(df)
    # print(df['<TP_SL>'].value_counts(normalize=True))

    # data_grp = df.groupby([df.index.date, '<TP_SL>'])
    # print(data_grp.first())
    #
    # data_grp = df.groupby([df.index.date, '<TP_SL>']).groups
    # print(data_grp)

    # data_grp = df.groupby('<TP_SL>')
    # df_g = data_grp.get_group(3)
    # print(df_g.head())

    data_grp = df.groupby([df.index.date, '<TP_SL>']).groups
    for i in data_grp:
        # i.count(-1)
        # print(type(i))
        print(i)
        # print(i['<TP_SL>'].value_counts(normalize=True))
        # print(i.count(-1))
        break

    # data_grp = df.groupby(df.index.date)
    # print(*data_grp, sep='\n\n')
    # print(data_grp.count)


if __name__ == "__main__":
    # Загружаем файл в DF
    file_path = Path(fr'c:\Users\Alkor\gd\data_quote\data_prepare_RTS_range_mvc_tpsl\SPFB.RTS_00_range250_splice_2021.txt')

    # Настройки отображения DF
    pd.set_option('max_rows', 15)  # Установка 5 строк вывода DF
    pd.set_option('display.max_columns', None)  # Сброс ограничений на число столбцов

    run(file_path)
