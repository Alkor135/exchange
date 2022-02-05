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


# def direction_tick_up(df_temp, last):
#     df_rev = df_temp.reindex(index=df_temp.index[::-1])
#     for line in df_rev.itertuples():
#         if line[3] < last:
#             return True
#         elif line[3] > last:
#             return False
#     return True


def run(tick_files: list, df: pd, delta_max_val: int, target_file_delta):

    for ind_file, tick_file in enumerate(tick_files):  # Итерация по файлам
        df_ticks_file: pd = pd.read_csv(tick_file, delimiter=',')  # Считываем тиковые данные в DF
        # print('\rCompleted: {:.2f}%'.format(ind_file * 100 / len(tick_file)), end='')
        previous_tick = 0
        direction_tick_up = True

        for tick in df_ticks_file.itertuples():  # Итерация по строкам тикового DF
            # print(f'{tick[1]} {tick[2]}')
            print('\rCompleted file: {:.2f}%. Completed files: {:.2f}%'.format(
                tick[0] * 100 / len(df_ticks_file.index),
                ind_file * 100 / len(tick_files)
                ),
                end=''
            )

            if tick[0] == 0:
                # Добавление строки в DF с дельта барами
                df.loc[len(df.index)] = [tick[1], tick[2], tick[3], tick[3], tick[3], tick[3], tick[4], 0]

            # Если бар сформирован по дельте и время открытия бара меньше времени текущего тика (защита от быстрого рынка)
            elif abs(df.iloc[-1]['<DELTA>']) >= delta_max_val and df.iloc[-1]['<TIME>'] < tick[2]:
                # Добавление строки в DF с дельта барами
                df.loc[len(df.index)] = [tick[1], tick[2], tick[3], tick[3], tick[3], tick[3], tick[4], 0]

            # Заполняем(изменяем) последнюю строку DF с дельта баром --------------------------------------
            # Записываем <CLOSE> --------------------------------------------------------------------------
            df.loc[len(df) - 1, '<CLOSE>'] = float(tick[3])  # Записываем последнюю цену как цену close бара

            # Записываем <HIGH> ---------------------------------------------------------------------------
            if float(tick[3]) > df.loc[len(df) - 1, '<HIGH>']:  # Если цена последнего тика больше чем high
                df.loc[len(df) - 1, '<HIGH>'] = float(tick[3])  # Записываем цену последнего тика как high

            # Записываем <LOW> ----------------------------------------------------------------------------
            if float(tick[3]) < df.loc[len(df) - 1, '<LOW>']:
                df.loc[len(df) - 1, '<LOW>'] = float(tick[3])  # Записываем цену последней сделки как low

            # Записываем <VOL> ----------------------------------------------------------------------------
            df.loc[len(df) - 1, '<VOL>'] += float(tick[4])  # Увеличиваем объем

            # Изменение дельты------------------------------------------------------------------------------------
            # Если направление тика на повышение
            if tick[3] > previous_tick:
                direction_tick_up = True
            elif tick[3] < previous_tick:
                direction_tick_up = False

            if direction_tick_up:
                df.iloc[-1]['<DELTA>'] += tick[4]  # Увеличиваем дельту на объем тика
            else:
                df.iloc[-1]['<DELTA>'] -= tick[4]  # Уменьшаем дельту на объем тика

            previous_tick = tick[3]

        # break

    df.to_csv(target_file_delta, index=False)


if __name__ == "__main__":
    ticker: str = 'RTS'
    year_tick: str = '2021'
    delta_max_val: int = 500
    source_dir_tick: Path = Path(f'c:/data_quote/data_finam_{ticker}_tick')
    target_file_delta: Path = Path(f'c:/data_quote/data_prepare_{ticker}_delta/{ticker}_{year_tick}_delta.csv')

    # Создание списка путей к файлам с тиками
    tick_files: list[Path] = list(source_dir_tick.glob(f'*{year_tick}*.csv'))

    # Создание DF под массив дельта баров
    df: pd = pd.DataFrame(columns='<DATE> <TIME> <OPEN> <HIGH> <LOW> <CLOSE> <VOL> <DELTA>'.split(' '))

    run(tick_files, df, delta_max_val, target_file_delta)


