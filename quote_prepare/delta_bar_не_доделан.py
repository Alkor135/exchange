"""
Скрипт из файлов с тиковыми данными делает файл с дельта барами
"""
import pandas as pd
from pathlib import *


class CurrentDeltaBar:
    def __init__(self):
        self.date = 0
        self.time = 0
        self.open = 0
        self.high = 0
        self.low = 0
        self.close = 0
        self.vol = 0
        self.delta = 0
        self.delta_time_sec = 0
        self.max_vol_cluster = 0
        self.max_volume = 0


def direction_tick_up(df_temp, last):
    df_rev = df_temp.reindex(index=df_temp.index[::-1])
    for line in df_rev.itertuples():
        if line[3] < last:
            return True
        elif line[3] > last:
            return False
    return True


def run(tick_files: list, df: pd, delta_max_val: int):

    # Создание DF из тиков для одного дельта бара для расчета макс объема в кластере
    df_ticks_bar: pd = pd.DataFrame(columns='<LAST> <VOL>'.split(' '))

    for tick_file in tick_files:  # Итерация по файлам
        df_ticks_file: pd = pd.read_csv(tick_file, delimiter=',')  # Считываем тиковые данные в DF

        for tick in df_ticks_file.itertuples():  # Итерация по строкам тикового DF
            # Если DF с дельта барами пустой(первая запись)
            if df.empty or abs(df.iloc[-1]['<DELTA>']) >= delta_max_val:
                # Добавление первой строки в DF с дельта барами
                df.loc[len(df.index)] = [tick[1], tick[2], tick[3], tick[3], tick[3], tick[3], tick[4], 0, 0, 0, 0]
                # Добавление первой строки в DF с тиками для дельта бара
                df_ticks_bar.loc[len(df_ticks_bar.index)] = [tick[3], tick[4]]

            # Если бар сформирован по дельте и время открытия бара меньше времени текущего тика (защита от быстрого рынка)
            elif abs(df.iloc[-1]['<DELTA>']) >= delta_max_val and df.iloc[-1]['<TIME>'] < tick[2]:
                # Заполняем <DELTA_TIME_SEC>

                # Заполняем <MAX_VOL_CLUSTER> <MAX_VOL>

                # Добавление строки в DF с дельта барами
                df.loc[len(df.index)] = [tick[1], tick[2], tick[3], tick[3], tick[3], tick[3], tick[4], 0, 0, 0, 0]
                # Обнуление df_ticks_bar
                df_ticks_bar = df_ticks_bar.iloc[0:0]
                # Добавление первой строки в DF с тиками для дельта бара
                df_ticks_bar.loc[len(df_ticks_bar.index)] = [tick[3], tick[4]]

            # Если направление тика на повышение
            if direction_tick_up(df_ticks_file[0:tick[1]]):
                df.iloc[-1]['<DELTA>'] += tick[4]  # Увеличиваем дельту на объем тика
            else:
                df.iloc[-1]['<DELTA>'] -= tick[4]  # Уменьшаем дельту на объем тика

            break
        # print(df_ticks_file)
        # print(df)

        break


if __name__ == "__main__":
    ticker: str = 'RTS'
    year_tick: str = '2021'
    delta_max_val: int = 500
    source_dir_tick: Path = Path(f'c:/data_quote/data_finam_{ticker}_tick')
    target_file_delta: Path = Path(f'c:/data_quote/data_prepare_{ticker}_delta/{ticker}_{year_tick}_delta.csv')

    # Создание списка путей к файлам с тиками
    tick_files: list[Path] = list(source_dir_tick.glob(f'*{year_tick}*.csv'))

    # Создание DF под массив дельта баров
    df = pd.DataFrame(columns='<DATE> <TIME> <OPEN> <HIGH> <LOW> <CLOSE> <VOL> <DELTA> <DELTA_TIME_SEC> '
                              '<MAX_VOL_CLUSTER> <MAX_VOL>'.split(' '))

    run(tick_files, df, delta_max_val)


