"""
Для расчета рендж баров эквивалентных 5 мин
"""
import re
from datetime import datetime
from pathlib import *

import pandas as pd
import numpy
import talib


def body(open, close):
        return abs(close - open)


if __name__ == "__main__":
    # 198 баров 5м в дне (с 7:00)

    period = 198
    source_file: Path = Path('c:\data_quote\data_finam_RTS_5m\SPFB.RTS_210301_220131.csv')
    df: pd = pd.read_csv(source_file, delimiter=',')  # Считываем тиковые данные в DF
    # Преобразуем столбец <TIME>, где нужно добавив 0 перед часом
    df['<BODY>'] = df.apply(lambda x: body(x['<OPEN>'], x['<CLOSE>']), axis=1)
    df['<RAZMER>'] = talib.MA(df['<BODY>'], timeperiod=period, matype=0)
    print(df)
    # print(real)

    """
    Получается, что рендж бар для фьючерса RTS должен быть размером 150, чтобы количество баров в дне, 
    примерно совпадало с с количеством 5 мин баров. 
    """
