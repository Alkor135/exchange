from pathlib import *
from datetime import datetime, timezone

import pandas as pd


# Загружаем файл в DF
df = pd.read_csv(
    Path(fr'c:\Users\Alkor\gd\data_quote\data_prepare_RTS_range_mvc_tpsl\SPFB.RTS_00_range250_splice_2021.txt'),
    delimiter=','
)
# Настройки отображения DF
pd.set_option('max_rows', 15)  # Установка 5 строк вывода DF
pd.set_option('display.max_columns', None)  # Сброс ограничений на число столбцов

# Удаляем ненужные колонки. axis=1 означает, что отбрасываем колонку а не индекс
df.drop(labels=['<MAX_VOLUME_PRICE>', '<MAX_VOLUME_CLUSTER>', '<TP_SL>'], axis=1, inplace=True)
# df.rename_axis(None, axis=1, inplace=True)
df.columns.name = None

print(df)

target_name = fr'c:\Users\Alkor\gd\data_quote\data_prepare_RTS_range_mvc_tpsl\RTS_00_range250_forex_tester_2021.txt'  # Создание имени новому файлу
df.to_csv(target_name, index=False)  # Запись в файл для одного файла
