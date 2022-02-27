"""
Cкрипт отрисовки графиков с макс volume cluster и TP/SL
"""
from pathlib import *
from datetime import datetime, timezone

import pandas as pd
import finplot as fplt

fplt.display_timezone = timezone.utc


def zero_hour(cell):
    """ Функция преобразует время (с финама приходят часы без нулей (с марта 2021), которые pandas не воспринимает)"""
    cell = f'{int(cell)}'
    tmp_time = datetime.strptime(cell, "%H%M%S")
    return tmp_time.strftime("%H%M%S")


def plot_candlestick(df, ax):
    df[['<OPEN>', '<CLOSE>', '<HIGH>', '<LOW>']].plot(ax=ax, kind='candle')  # рисуем свечной график в основном окне
    df['<MAX_VOLUME_PRICE>'].plot(kind='scatter', style='o', color='#00f', ax=ax)  # Отметки на графике макс объемов в кластере


def plot_tpsl(df, ax):
    """ Отрисовка ТП/СЛ """
    df['<TP_SL>'].plot(ax=ax, kind='bar', legend='TP_SL')  #


def plot_ema(df, ax):
    """Отрисовка индикатора ЕМА"""
    df['<CLOSE>'].ewm(span=18).mean().plot(ax=ax, legend='EMA')


if __name__ == "__main__":
    symbol = 'RTS'
    edge_only = True
    # Формат файла
    """
    <DATE>,<TIME>,<OPEN>,<HIGH>,<LOW>,<CLOSE>,<VOL>,<MAX_VOLUME_PRICE>,<MAX_VOLUME_CLUSTER>,<TP_SL>
    20220119,70000,137360.0,137600.0,137350.0,137600.0,15,137350.0,2,-1
    20220119,70001,137770.0,137770.0,137520.0,137520.0,204,137360.0,102,3
    20220119,70002,137290.0,137270.0,137020.0,137270.0,268,137100.0,39,-1
    """
    # Загружаем файл в DF
    df = pd.read_csv(
        # Path('fr'c:\Users\Alkor\gd\data_quote\data_prepare_RTS_range_mvc_tpsl\SPFB.RTS_range250_mvc_tpsl_20220119.txt'),
        Path(fr'c:\Users\Alkor\gd\data_quote\data_prepare_RTS_range_mvc_tpsl\SPFB.RTS_00_range250_splice_2021.txt'),
        delimiter=','
    )
    # Настройки отображения DF
    pd.set_option('max_rows', 5)  # Установка 5 строк вывода DF
    pd.set_option('display.max_columns', None)  # Сброс ограничений на число столбцов

    # Обработка DF
    df['<TIME>'] = df.apply(lambda x: zero_hour(x['<TIME>']), axis=1)  # Преобразуем столбец <TIME>, где нужно добавив 0 перед часом
    df['<DATE_TIME>'] = df['<DATE>'].astype(str) + ' ' + df['<TIME>'].astype(str)  # Создаем новый столбец <DATE_TIME> слиянием столбцов <DATE> и <TIME>
    df = df.set_index(pd.DatetimeIndex(df['<DATE_TIME>']))  # Меняем индекс и делаем его типом datetime
    df.drop(labels=['<DATE_TIME>', '<DATE>', '<TIME>', '<VOL>'], axis=1, inplace=True)  # Удаляем ненужные колонки. axis=1 означает, что отбрасываем колонку а не индекс

    if edge_only:

    print(df)

    # Построение графика
    ax1, ax2 = fplt.create_plot(symbol, rows=2)  # Cоздаем окна
    plot_tpsl(df, ax2)  #
    plot_candlestick(df, ax1)  # рисуем свечной график в основном окне
    plot_ema(df, ax1)

    ax2.setXLink(ax1)  # Для синхронизации осей Х

    fplt.show()
