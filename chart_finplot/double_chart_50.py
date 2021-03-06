#!/usr/bin/env python3

from pathlib import *
from datetime import datetime, timezone
import finplot as fplt
from functools import lru_cache
from PyQt5.QtWidgets import QApplication, QGridLayout, QMainWindow, QGraphicsView, QComboBox, QLabel
from pyqtgraph.dockarea import DockArea, Dock
from threading import Thread
import yfinance as yf
import pandas as pd

app = QApplication([])
win = QMainWindow()
area = DockArea()
win.setCentralWidget(area)
win.resize(1600, 800)
win.setWindowTitle("Docking charts example for finplot")

# Set width/height of QSplitter
win.setStyleSheet("QSplitter { width : 20px; height : 20px; }")

# Create docks
dock_0 = Dock("dock_0", size = (1000, 100), closable = True)
dock_1 = Dock("dock_1", size = (1000, 100), closable = True)
# dock_2 = Dock("dock_2", size = (1000, 100), closable = True)
area.addDock(dock_0)
area.addDock(dock_1)

# Chart for dock_0
ax0, ax1 = fplt.create_plot_widget(master=area, rows=2, init_zoom_periods=100)  # ,ax2
area.axs = [ax0, ax1]  #, ax2
dock_0.addWidget(ax0.ax_widget, 1, 0, 1, 2)
dock_1.addWidget(ax1.ax_widget, 1, 0, 1, 2)

# Link x-axis
ax1.setXLink(ax0)
win.axs = [ax0]

plots = []

fplt.display_timezone = timezone.utc

# symbol = 'RTS'
# Загружаем файлы в DF
df_first = pd.read_csv(
    Path('c:\data_quote\data_prepare_VTBR_5m\VTBR_2021.csv'),
    delimiter=','
)
df_second = pd.read_csv(
    Path('c:\data_quote\data_prepare_SBER_5m\SBER_2021.csv'),
    delimiter=','
)


pd.set_option('max_rows', 5)  # Установка 5 строк вывода DF
pd.set_option('display.max_columns', None)  # Сброс ограничений на число столбцов


def zero_hour(cell):
    """ Функция преобразует время (с финама приходят часы без нулей (с декабря 2021), которые pandas не воспринимает)"""
    cell = f'{int(cell)}'
    tmp_time = datetime.strptime(cell, "%H%M%S")
    return tmp_time.strftime("%H%M%S")


def plot_ema(df, ax):
    df['<CLOSE>'].ewm(span=18).mean().plot(ax=ax, legend='EMA')


def prepare(df):
    # Преобразуем столбец <TIME>, где нужно добавив 0 перед часом
    df['<TIME>'] = df.apply(lambda x: zero_hour(x['<TIME>']), axis=1)
    # Создаем новый столбец <DATE_TIME> слиянием столбцов <DATE> и <TIME>
    df['<DATE_TIME>'] = df['<DATE>'].astype(str) + ' ' + df['<TIME>'].astype(str)
    # Меняем индекс и делаем его типом datetime
    df = df.set_index(pd.DatetimeIndex(df['<DATE_TIME>']))
    # Удаляем ненужные колонки. axis=1 означает, что отбрасываем колонку а не индекс
    df.drop(labels=['<DATE_TIME>', '<DATE>', '<TIME>', '<VOL>'], axis=1, inplace=True)
    # return df[['<OPEN>', '<CLOSE>', '<HIGH>', '<LOW>']]


df_first = prepare(df_first)
df_second = prepare(df_second)
candles_first = df_first[['<OPEN>', '<CLOSE>', '<HIGH>', '<LOW>']]
candles_second = df_second[['<OPEN>', '<CLOSE>', '<HIGH>', '<LOW>']]
fplt.candlestick_ochl(candles_first(df_first), ax=ax0)
fplt.candlestick_ochl(candles_second(df_second), ax=ax1)

df_first.plot('<MAX_VOLUME_PRICE>', kind='scatter', style='o', color='#00f', ax=ax0)
df_second.plot('<MAX_VOLUME_PRICE>', kind='scatter', style='o', color='#00f', ax=ax1)

fplt.show(qt_exec=False)  # prepares plots when they're all setup
win.show()
app.exec_()
