"""
Скрипт из файлов с тиковыми данными делает файл с дельта барами
"""
import pandas as pd
from pathlib import *


def run(tick_files, df):
    print(tick_files)
    for tick_file in tick_files:
        print(tick_file)
        df_tick = pd.read_csv(tick_file, delimiter=',')  # Считываем тиковые данные в DF
        print(df_tick)
        for tick in df_tick.itertuples():
            print(tick)
            break
        break


if __name__ == "__main__":
    ticker = 'RTS'
    year_tick = '2021'
    source_dir_tick: Path = Path(f'c:\data_quote\data_finam_{ticker}_tick')
    target_file_delta: Path = Path(f'c:\data_quote\data_prepare_{ticker}_delta\\{ticker}_{year_tick}_delta.csv')

    # Создание списка путей к файлам с тиками
    tick_files: list[Path] = list(source_dir_tick.glob(f'*{year_tick}*.csv'))

    df = pd.DataFrame()
    run(tick_files, df)


