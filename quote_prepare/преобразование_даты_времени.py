"""
Проба формата времени
"""
from datetime import datetime

import pandas as pd

# Загрузка в DF range файла
df: pd = pd.read_csv('c:\data_quote\data_prepare_RTS_range_mvc_tpsl\SPFB.RTS_range250_mvc_tpsl_20210304.txt',
                     delimiter=',')

# print(df)
print(f"{df.loc[0, '<DATE>']=}, {df.loc[0, '<TIME>']=}")
current_dt = f"{df.loc[0, '<DATE>']} {df.loc[0, '<TIME>']}"
current_dt = datetime.strptime(current_dt, '%Y%m%d %H%M%S')
print(current_dt)

next_dt = f"{df.loc[1, '<DATE>']} {df.loc[1, '<TIME>']}"
next_dt = datetime.strptime(next_dt, '%Y%m%d %H%M%S')
print(next_dt)

print(next_dt - current_dt)
print((next_dt - current_dt).total_seconds())
