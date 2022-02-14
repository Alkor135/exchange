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
    # fplt.candlestick_ochl(df[['<OPEN>', '<CLOSE>', '<HIGH>', '<LOW>']], ax=ax)  # рисуем свечной график в основном окне
    df[['<OPEN>', '<CLOSE>', '<HIGH>', '<LOW>']].plot(ax=ax, kind='candle')
    # fplt.plot(df['<MAX_VOLUME_PRICE>'], kind='scatter', style='o', color='#00f', ax=ax)  # Отметки на графике макс объемов в кластере
    df['<MAX_VOLUME_PRICE>'].plot(kind='scatter', style='o', color='#00f', ax=ax)


def plot_tpsl(df, ax):
    df['<TP_SL>'].plot(ax=ax, kind='bar')  # Не синхронный масштаб. отображение отличное  , kind='bar'


def plot_tpsl1(df, ax):
    df['<TP_SL>'].plot(ax=ax)  # Не синхронный масштаб. отображение отличное  , kind='bar'


if __name__ == "__main__":
    symbol = 'RTS'
    # Формат файла
    """
    <DATE>,<TIME>,<OPEN>,<HIGH>,<LOW>,<CLOSE>,<VOL>,<MAX_VOLUME_PRICE>,<MAX_VOLUME_CLUSTER>,<TP_SL>
    20220119,70000,137360.0,137600.0,137350.0,137600.0,15,137350.0,2,-1
    20220119,70001,137770.0,137770.0,137520.0,137520.0,204,137360.0,102,3
    20220119,70002,137290.0,137270.0,137020.0,137270.0,268,137100.0,39,-1
    """
    # Загружаем файл в DF
    df = pd.read_csv(
        Path('c:\data_quote\data_prepare_RTS_range_mvc_tpsl\SPFB.RTS_range250_mvc_tpsl_20220103.txt'),
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
    print(df)

    # Построение графика
    ax1, ax2, ax3 = fplt.create_plot(symbol, rows=3)  # Cоздаем окна
    plot_tpsl(df, ax2)  #
    plot_tpsl1(df, ax3)  #
    plot_candlestick(df, ax1)  # рисуем свечной график в основном окне



    # Рисуем TPSL
    # fplt.volume_ocv(df[['<OPEN>', '<CLOSE>', '<TP_SL>']], ax=ax2)  # Рисуется только в плюс
    # fplt.volume_ocv(df[['<OPEN>', '<CLOSE>', '<TP_SL>']], kind='bar', ax=ax2)  # Ошибка
    # fplt.bar(df[['<OPEN>', '<CLOSE>', '<TP_SL>']], ax=ax2)  # Вообще ничего не видно
    # fplt.bar(df['<TP_SL>'], ax=ax2)  # Не синхронный масштаб. отображение отличное
    # fplt.bar(df[['<TP_SL>']], ax=ax2)  # Не синхронный масштаб. отображение отличное
    # fplt.plot(df['<TP_SL>'], ax=ax2, kind='bar')  # Отрисовка линиями
    # fplt.plot(df[['<TP_SL>']], ax=ax2, kind='bar')  # Отрисовка линиями

    # df.plot('<TP_SL>', kind='candle', ax=ax2)  # Не то
    # df.plot('<TP_SL>', kind='volume', ax=ax2)  # Ничего не видно
    # df.plot('<TP_SL>', kind='bar', ax=ax2)  # Не синхронный масштаб. отображение отличное
    # df['<TP_SL>'].plot.bar(ax=ax2)  # Не синхронный масштаб. отображение отличное

    # fplt.volume_ocv(df[['<OPEN>', '<CLOSE>', '<TP_SL>']], ax=ax2)
    # fplt.bar(df['<TP_SL>'], ax=ax2)

    fplt.show()
