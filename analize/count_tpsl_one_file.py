"""
Скрипт собирает статистику по одному файлу ТПСЛ
"""
import re
from pathlib import *

import pandas as pd


def run(source_file):

    df = pd.read_csv(source_file, delimiter=',')  # Считываем данные в DF

    df = df.loc[df['<TP_SL>'] != 0]  # Убираем строки где <TP_SL> равен 0 (конец дня)
    # Убираем строки где кластер с макс объемом вне бара (быстрое движение рынка)
    df = df.loc[df['<HIGH>'] > df['<MAX_VOLUME_PRICE>']]
    df = df.loc[df['<MAX_VOLUME_PRICE>'] > df['<LOW>']]

    # df = df.loc[(df['<TIME>'] >= 90000) & (df['<TIME>'] < 100000)]  # Выборка по значениям (по времени)

    print('\n', source_file.name)
    print(df['<TP_SL>'].value_counts())
    print(df['<TP_SL>'].value_counts(normalize=True))


if __name__ == "__main__":
    # Путь к файлу

    source_file1: Path = Path(
        fr'c:\Users\Alkor\gd\data_quote\data_prepare_RTS_range_mvc_tpsl_sec\SPFB.RTS_00_range250_splice_2021.txt')
    source_file2: Path = Path(
        fr'c:\Users\Alkor\gd\data_quote\data_prepare_RTS_range_mvc_tpsl_sec\SPFB.RTS_00_range250_splice_2022.txt')

    run(source_file1)
    run(source_file2)
