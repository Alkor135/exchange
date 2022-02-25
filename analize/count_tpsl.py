"""
Скрипт собирает статистику по файлам ТПСЛ
"""
import re
from pathlib import *

import pandas as pd


def run(files_path, razmer, year):

    df_total: pd = pd.DataFrame()
    raznica = 0

    for ind_file, file in enumerate(files_path, start=1):  # Итерация по тиковым файлам

        # Парсинг имени файла
        list_split = re.split('_', file.name, maxsplit=0)  # Разделение имени файла по '_'
        tiker = list_split[0]  # Получение тикера из имени файла

        df = pd.read_csv(file, delimiter=',')  # Считываем данные в DF

        df = df.loc[(df['<TIME>'] >= 90000) & (df['<TIME>'] < 100000)]  # Выборка по значениям (по времени)

        rez = df['<TP_SL>'].value_counts()  # DF с количеством по профитности
        print('\n', file.name)
        # print(df['<TP_SL>'].value_counts())
        print(df['<TP_SL>'].value_counts(normalize=True))

        df_total = df_total.append(df)

        # break

    print('\nИтого')
    print(df_total['<TP_SL>'].value_counts())
    print(df_total['<TP_SL>'].value_counts(normalize=True))


if __name__ == "__main__":
    razmer: int = 250
    ticker: str = 'RTS'
    year: str = '2022'

    source_dir: Path = Path(fr'c:\Users\Alkor\gd\data_quote\data_prepare_{ticker}_range_mvc_tpsl')  # Путь к ресурсному каталогу

    # Создание списка путей к файлам
    files_path: list[Path] = list(source_dir.glob(f'*{razmer}*{year}*.txt'))

    run(files_path, razmer, year)
