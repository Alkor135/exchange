"""
Подсчет доходности инструмента WIMM в процентах в месяц и на основе месяца расчет в годовых
"""

import pandas as pd


def percent(df: pd) -> pd:
    """ Функция подсчитывает доходность в процентах в месяц и доходность в годовых для этого месяца"""
    previous_close: float = 0.0
    for val in df.itertuples():  # Итерация по строкам DF
        current_close: float = val[2]
        if previous_close != 0.0:
            profit: float = current_close - previous_close
            df.loc[val[0], '<PERCENT_MONTHLY>']: pd[float] = profit * 100 / previous_close
            df.loc[val[0], '<PERCENT_YEAR>']: pd[float] = df.loc[val[0], '<PERCENT_MONTHLY>'] * 12
        previous_close = current_close
    return df


if __name__ == "__main__":
    # Загрузка в DF данные из файла
    df: pd = pd.read_csv('c:/Users/Alkor/gd/data_quote/WIMM/VTBM_200330_220528.csv', delimiter=',')
    # df: pd = pd.read_csv('c:/Users/Alkor/gd/data_quote/WIMM/SBMM_200330_220528.csv', delimiter=',')
    # df: pd = pd.read_csv('c:/Users/Alkor/gd/data_quote/WIMM/RCMM_200330_220528.csv', delimiter=',')

    # Замена формата колонки <DATE>
    df['<DATE>'] = pd.to_datetime(df['<DATE>'], format='%Y%m%d')

    # Создание DF с максимальными датами в месяце
    df = df.resample(on='<DATE>', rule="M").max().reset_index(drop=True)

    # Удаление ненужных колонок
    df: pd = df.drop(labels=['<TICKER>', '<PER>', '<TIME>'], axis='columns')

    # Подсчет доходности
    df = percent(df)

    print(df)
