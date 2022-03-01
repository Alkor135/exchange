"""
Cкрипт отрисовки графиков с макс volume cluster и TP/SL
"""
from typing import Any
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


def plot_vol(df, ax):
    """ Отрисовка ТП/СЛ """
    df['<VOL>'].plot(ax=ax, kind='bar', legend='VOLUME')  #


def plot_ema(df, ax, period):
    """Отрисовка индикатора ЕМА"""
    df['<CLOSE>'].ewm(span=period).mean().plot(ax=ax, legend=f'EMA {period}')


def edge_prepare(df: pd, edge_only: Any):
    """ Функция меняет значения колонки TP_SL, если не удовлетворяет перцентилю записывается 0"""
    def replace_cell(high: float, low: float, close: float, mvc: float, tpsl: int) -> int:
        df_tmp = pd.DataFrame({'field': [low, high]})
        if low <= mvc <= high:  # Если макс объем в баре (защита от ошибочных баров)
            if close == high:  # Если бар на повышение
                val = df_tmp['field'].quantile(edge_only)  # Перцентиль
                if mvc <= val:
                    return tpsl
            elif close == low:  # Если бар на понижение
                val = df_tmp['field'].quantile(1 - edge_only)  # Перцентиль
                if mvc >= val:
                    return tpsl
        return 0

    df['<TP_SL>'] = df.apply(lambda x: replace_cell(x['<HIGH>'],
                                                    x['<LOW>'],
                                                    x['<CLOSE>'],
                                                    x['<MAX_VOLUME_PRICE>'],
                                                    x['<TP_SL>']),
                             axis=1)
    return df


if __name__ == "__main__":
    symbol = 'RTS'
    edge_only = 0.0  # Значение установить в 0 если не нужны перцентили ТП/СЛ
    ema_period = 18
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
    pd.set_option('max_rows', 15)  # Установка 5 строк вывода DF
    pd.set_option('display.max_columns', None)  # Сброс ограничений на число столбцов

    # Обработка DF
    df['<EMA>'] = df['<CLOSE>'].ewm(span=ema_period, adjust=False).mean()
    df['<TIME>'] = df.apply(lambda x: zero_hour(x['<TIME>']), axis=1)  # Преобразуем столбец <TIME>, где нужно добавив 0 перед часом
    df['<DATE_TIME>'] = df['<DATE>'].astype(str) + ' ' + df['<TIME>'].astype(str)  # Создаем новый столбец <DATE_TIME> слиянием столбцов <DATE> и <TIME>
    df = df.set_index(pd.DatetimeIndex(df['<DATE_TIME>']))  # Меняем индекс и делаем его типом datetime
    df.drop(labels=['<DATE_TIME>', '<DATE>', '<TIME>'], axis=1, inplace=True)  # Удаляем ненужные колонки. axis=1 означает, что отбрасываем колонку а не индекс

    if edge_only != 0:
        df_tpsl = edge_prepare(df, edge_only)

    # print(df)

    df_new = df.loc[df['<TP_SL>'] != 0]  # Выбираются только строки удовлетворяющие перцентилю MVC

    df_up = df_new.loc[df_new['<LOW>'] >= df_new['<EMA>']]  # EMA
    df_up = df_up.loc[df_up['<CLOSE>'] == df_up['<HIGH>']]  # Бар на повышение

    df_down = df_new.loc[df_new['<HIGH>'] <= df_new['<EMA>']]  # EMA
    df_down = df_down.loc[df_down['<CLOSE>'] <= df_down['<LOW>']]  # Бар на понижение
    # print(df_new)

    print('\nВыше ЕМА')
    print(df_up['<TP_SL>'].value_counts())
    print(df_up['<TP_SL>'].value_counts(normalize=True))

    print('\nНиже EMA')
    print(df_down['<TP_SL>'].value_counts())
    print(df_down['<TP_SL>'].value_counts(normalize=True))

    # Построение графика
    ax1, ax2, ax3 = fplt.create_plot(symbol, rows=3)  # Cоздаем окна
    plot_tpsl(df, ax2)  #
    plot_vol(df, ax3)  #
    plot_candlestick(df, ax1)  # рисуем свечной график в основном окне
    plot_ema(df, ax1, ema_period)

    ax2.setXLink(ax1)  # Для синхронизации осей Х
    ax3.setXLink(ax1)  # Для синхронизации осей Х

    fplt.show()
