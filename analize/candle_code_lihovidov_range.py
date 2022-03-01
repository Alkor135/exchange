"""
Скрипт добавляет к DF с рандже барами колонку кода свечи по Лиховидову
"""
import re
from pathlib import *
from datetime import datetime
from typing import Any

import pandas as pd
import numpy as np


def clearing_df(df: pd):
    """Функция очистки DF"""
    df = df.loc[df['<TP_SL>'] != 0]  # Убираем строки где <TP_SL> равен 0 (конец дня)
    # Убираем строки где кластер с макс объемом вне бара (быстрое движение рынка)
    df = df.loc[df['<HIGH>'] > df['<MAX_VOLUME_PRICE>']]
    df = df.loc[df['<MAX_VOLUME_PRICE>'] > df['<LOW>']]
    return df


def candle_code(open, high, low, close):
    code_str: str = ''
    df_tmp = pd.DataFrame({'max_min': [high, low]})
    if close == high:
        code_str += '1'
        if df_tmp['max_min'].quantile(.66) < open:
            code_str += '11'
        elif df_tmp['max_min'].quantile(.33) <= open:
            code_str += '10'
        elif df_tmp['max_min'].quantile(.33) > open:
            code_str += '01'
    elif close == low:
        code_str += '0'
        if df_tmp['max_min'].quantile(.66) < open:
            code_str += '10'
        elif df_tmp['max_min'].quantile(.33) <= open:
            code_str += '01'
        elif df_tmp['max_min'].quantile(.33) > open:
            code_str += '00'
    return int(code_str, base=2)


def candle_code_range(df: pd):
    df = clearing_df(df)  # Очистка DF
    df['<CC>'] = np.nan  # Создание дополнительного столбца под код свечи и заполнение его NaN
    # columns_lst: list = list(df.columns.values)
    # print(columns_lst)
    df['<CC>'] = df.apply(lambda x: candle_code(x['<OPEN>'],
                                                x['<HIGH>'],
                                                x['<LOW>'],
                                                x['<CLOSE>']),
                          axis=1)  # Заполняем столбец СС

    df = df.loc[df['<CC>'] != '']  # Убираем строки где <CC> равен пустой строке
    return df


if __name__ == "__main__":
    # Путь к файлу
    source_file: Path = Path(
        fr'c:\Users\Alkor\gd\data_quote\data_prepare_RTS_range_mvc_tpsl_sec\SPFB.RTS_00_range250_splice_2021.txt')

    # Настройки отображения DF
    pd.set_option('max_rows', 15)  # Установка 5 строк вывода DF
    pd.set_option('display.max_columns', None)  # Сброс ограничений на число столбцов

    df: pd = pd.read_csv(source_file, delimiter=',')  # Считываем данные в DF
    # print(df)
    df = candle_code_range(df)
    # print(df)
    df = df.loc[df['<HIGH>'] == df['<CLOSE>']]  # Только бары на повышение
    print(df['<CC>'].value_counts())
    print(df['<CC>'].value_counts(normalize=True))

    df = df.loc[df['<TP_SL>'] > 0]  # Только прибыльные бары
    print(df['<CC>'].value_counts())
    print(df['<CC>'].value_counts(normalize=True))

    # df = df.loc[df['<HIGH>'] == df['<CLOSE>']]  # Только бары на повышение
    # print(df['<CC>'].value_counts())
    # print(df['<CC>'].value_counts(normalize=True))
