"""
Универсальный скрипт отрисовки графиков
"""
from pathlib import *
from datetime import datetime, timezone

import pandas as pd
import finplot as fplt

fplt.display_timezone = timezone.utc

symbol = 'RTS'
# Загружаем файл в DF
# Формат файла
"""
<DATE>,<TIME>,<OPEN>,<HIGH>,<LOW>,<CLOSE>,<VOL>,<DELTA>
20210104,100000,139240.0,140220.0,139240.0,140220.0,504,501
20210104,100001,140230.0,140670.0,139750.0,140670.0,1797,503
20210104,100005,140530.0,141150.0,140530.0,140900.0,2851,-511
20210104,100016,140890.0,141000.0,140800.0,141000.0,1390,515
"""
df = pd.read_csv(Path('c:\data_quote\data_prepare_RTS_delta\SPFB.RTS_delta_20220119.csv'), delimiter=',')

pd.set_option('max_rows', 5)  # Установка 5 строк вывода DF
pd.set_option('display.max_columns', None)  # Сброс ограничений на число столбцов


def zero_hour(cell):
    """ Функция преобразует время (с финама приходят часы без нулей (с декабря 2021), которые pandas не воспринимает)"""
    cell = f'{int(cell)}'
    tmp_time = datetime.strptime(cell, "%H%M%S")
    return tmp_time.strftime("%H%M%S")


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

# создаем 4 окна
ax = fplt.create_plot(symbol, rows=1)

# рисуем свечной график в основном окне
candles = df[['<OPEN>', '<CLOSE>', '<HIGH>', '<LOW>']]
fplt.candlestick_ochl(candles, ax=ax)

# # рисуем график времени дельты свечи
# delta_time = df[['open', 'close', 'delta_time']]
# fplt.volume_ocv(delta_time, ax=ax2)
#
# # рисуем график дельты
# delta = df[['open', 'close', 'delta']]
# fplt.volume_ocv(delta, ax=ax3)

# Проба дополнить график точками (нужно в будущем для отметки на графике макс объемов в кластере)
# df.plot('<MAX_VOLUME_PRICE>', kind='scatter', style='o', color='#00f')

fplt.show()