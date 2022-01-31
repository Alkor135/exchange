"""
Подготовка данных 5 минутных котировок.
Берется файл с 5мин данными и файлы с тиковыми данными.
Из тиковых данных расcчитывается кластер с максимальными объемами и дописывается столбцом к 5мин данным.
Полученный массив данных сохраняется в новый файл, для последующего анализа и построения графиков.
"""
import os

import pandas as pd
import numpy as np
from pathlib import *



pd.set_option('max_rows', 5)
# Создание df для 5 мин баров
df_5m: pd = pd.read_csv(Path('c:\data_quote\data_finam_RTS_5m\SPFB.RTS_2020.csv'), delimiter=',')

tick_files: list[Path] = list(Path('c:\data_quote\data_finam_RTS_tick').glob('*'))
# print(tick_files)

df_tick: pd = pd.DataFrame
isempty = df_tick.empty

print(isempty)

# for row_5m in df_5m.itertuples():
#     if len(df_tick.index) == 0 or df_5m.iloc[0][0] != df_tick.iloc[0][0]:
#         tick_file = [file for file in tick_files if str(row_5m[1]) in str(file)]
#         if len(tick_file) > 0:
#             df_tick = pd.read_csv(Path(tick_file[0]), delimiter=',')
#         print(df_tick)
#
#         print(tick_file)
#         print(*tick_file)
#         print(row_5m)
#         print(str(row_5m[1]))
#         break

# print(int(df_5m.iloc[0][0]))
# print(df_5m)

# # Создание списка тиковых файлов
# files: list[Path] = list(Path('c:\data_quote\data_finam_RTS_tick').glob('*'))
# # print(files)
# df_tick: pd = pd.read_csv(Path(files[0]), delimiter=',')
# print(df_tick)
