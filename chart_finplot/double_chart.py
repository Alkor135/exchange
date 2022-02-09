"""
Универсальный скрипт отрисовки графиков
"""
from pathlib import *
from datetime import datetime, timezone

import pandas as pd
import numpy as np
import finplot as fplt

fplt.display_timezone = timezone.utc

symbol = 'RTS'
# Загружаем файл в DF
# Формат файла
"""

"""
# df = pd.read_csv(Path('c:\data_quote\data_prepare_RTS_delta\SPFB.RTS_delta_20220119.csv'), delimiter=',')
df = pd.read_csv(Path('c:\data_quote\data_prepare_RTS_range_max_vol\SPFB.RTS_range250_max_vol_20220103.txt'), delimiter=',')

pd.set_option('max_rows', 5)  # Установка 5 строк вывода DF
pd.set_option('display.max_columns', None)  # Сброс ограничений на число столбцов


def zero_hour(cell):
    """ Функция преобразует время (с финама приходят часы без нулей (с декабря 2021), которые pandas не воспринимает)"""
    cell = f'{int(cell)}'
    tmp_time = datetime.strptime(cell, "%H%M%S")
    return tmp_time.strftime("%H%M%S")


def plot_ema(df, ax):
    df['<CLOSE>'].ewm(span=18).mean().plot(ax=ax, legend='EMA')


# def plot_bubble_pass(price, price_col, size_col, min_val, max_val, scale, color, ax):
#     price = price.copy()
#     price.loc[(price[size_col] < min_val) | (price[size_col] > max_val), price_col] = np.nan
#     fplt.plot(price[price_col], style='o', width=scale, color=color, ax=ax)
#
#
# def plot_quote_bubbles(quotes, ax):
#     quotes['mvc'] = np.sqrt(quotes['<MAX_VOLUME_CLUSTER>'])  # linearize by circle area
#     size = quotes['mvc']
#     rng = np.linspace(size.min(), size.max(), 5)
#     rng = list(zip(rng[:-1], rng[1:]))
#     for a, b in reversed(rng):
#         scale = (a+b) / rng[-1][1] + 0.2
#         plot_bubble_pass(quotes, '<MAX_VOLUME_PRICE>', '<MAX_VOLUME_CLUSTER>', a, b, scale=scale, color='#00f', ax=ax)


# Преобразуем столбец <TIME>, где нужно добавив 0 перед часом
df['<TIME>'] = df.apply(lambda x: zero_hour(x['<TIME>']), axis=1)

# Создаем новый столбец <DATE_TIME> слиянием столбцов <DATE> и <TIME>
df['<DATE_TIME>'] = df['<DATE>'].astype(str) + ' ' + df['<TIME>'].astype(str)
# print(df)

# Меняем индекс и делаем его типом datetime
df = df.set_index(pd.DatetimeIndex(df['<DATE_TIME>']))
# print(df)

# Удаляем ненужные колонки. axis=1 означает, что отбрасываем колонку а не индекс
df.drop(labels=['<DATE_TIME>', '<DATE>', '<TIME>', '<VOL>'], axis=1, inplace=True)
print(df)

# создаем окна
ax, ax1 = fplt.create_plot(symbol, rows=2)
ax.set_visible(xgrid=False, ygrid=True)

# рисуем свечной график в основном окне
candles = df[['<OPEN>', '<CLOSE>', '<HIGH>', '<LOW>']]
fplt.candlestick_ochl(candles, ax=ax)
fplt.candlestick_ochl(candles, ax=ax1)

# EMA
plot_ema(df, ax)

# # Макс объем в кластере
df.plot('<MAX_VOLUME_PRICE>', kind='scatter', style='o', color='#00f')
# plot_quote_bubbles(df, ax=ax)

fplt.show()
