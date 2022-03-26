"""
Cкрипт торговой стратегии
"""
from typing import Any
from pathlib import *
from datetime import datetime, timezone

import pandas as pd


class Position:
    positions = []  # Список экземпляров класса

    def __init__(self, open_time, open_price, tp, sl, koef):
        """Инициализация"""
        self.open_time = open_time
        self.open_price = open_price
        self.tp = tp
        self.sl = sl
        self.koef = koef
        self.direction = 'None'
        Position.positions.append(self)  # Добавление в список экземпляров класса

    def __str__(self):
        return "{} {}".format(self.open_time, self.open_price)


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


def close(high, low):
    if len(Position.positions) != 0:
        for pos in Position.positions:
            if low <= pos.sl:
                total_rez -= 1
                Position.positions.pop(pos)
            elif high > pos.tp:
                total_rez += pos.koef
                Position.positions.pop(pos)



def run(df):
    df = dataframe_datetime_conversion(df)
    columns = list(df.columns)
    print(*columns)
    for row in df.itertuples():  # Итерация по рандже барам
        if row[columns.index('<HIGH>') + 1] == row[columns.index('<CLOSE>') + 1]:
            close(row[columns.index('<HIGH>') + 1], row[columns.index('<LOW>') + 1])
        # if row[columns.index('<CLOSE>')+1] == row[columns.index('<HIGH>')+1]:  # Если бар на повышение


if __name__ == "__main__":
    # Загружаем файл в DF
    df = pd.read_csv(
        Path(fr'c:\Users\Alkor\gd\data_quote\data_prepare_RTS_range_mvc_tpsl\SPFB.RTS_00_range250_splice_2021.txt'),
        delimiter=','
    )
    # Настройки отображения DF
    pd.set_option('max_rows', 15)  # Установка 5 строк вывода DF
    pd.set_option('display.max_columns', None)  # Сброс ограничений на число столбцов

    total_rez = 0
    run(df)
