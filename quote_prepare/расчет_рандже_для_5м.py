"""
Для расчета рендж баров эквивалентных 5 мин
"""
from pathlib import *

import pandas as pd
import talib


def body(open: float, close: float) -> float:
        return abs(close - open)


if __name__ == "__main__":
    # 198 баров 5м в дне (с 7:00)

    period: int = 198
    source_file: Path = Path('c:\data_quote\data_finam_RTS_5m\SPFB.RTS_210301_220131.csv')
    df: pd = pd.read_csv(source_file, delimiter=',')  # Считываем тиковые данные в DF

    df['<BODY>'] = df.apply(lambda x: body(x['<OPEN>'], x['<CLOSE>']), axis=1)
    df['<RAZMER>'] = talib.MA(df['<BODY>'], timeperiod=period, matype=0)

    df_15: pd = df.loc[df['<TIME>'] == 150000]  # Бары в 15:00

    print(df_15.tail(20))

    """
    Получается, что рендж бар для фьючерса RTS должен быть размером 250, чтобы количество баров в дне, 
    примерно совпадало с с количеством 5 мин баров. 
    """
