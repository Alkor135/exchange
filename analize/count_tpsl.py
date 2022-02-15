"""
Скрипт собирает статистику по файлам ТПСЛ
"""
import re
from pathlib import *

import pandas as pd


def run(files_path, razmer, year):

    result: pd = pd.DataFrame()
    tiker: str = ''
    raznica = 0
    for ind_file, file in enumerate(files_path, start=1):  # Итерация по тиковым файлам
        # print('\rCompleted files: {:.2f}%'.format(ind_file * 100 / len(files_path)), end='')  # Прогресс

        # Парсинг имени файла
        list_split = re.split('_', file.name, maxsplit=0)  # Разделение имени файла по '_'
        tiker = list_split[0]  # Получение тикера из имени файла

        df = pd.read_csv(file, delimiter=',')  # Считываем данные в DF

        rez = df['<TP_SL>'].value_counts()
        print(file.name)
        print(df['<TP_SL>'].value_counts())
        print(df['<TP_SL>'].value_counts(normalize=True))
        # print(df['<TP_SL>'].value_counts().idxmax())  # Индекс максимального по количеству
        print(f'-1:{rez[-1]}, +1:{rez[3]+rez[1]+rez[2]}   Разница: {rez[3]*3-(rez[-1]+rez[1]+rez[2])}\n')
        raznica += (rez[3]*3-(rez[-1]+rez[1]+rez[2]))
        # print(df.groupby('<TIME>')['<TP_SL>'].value_counts())
        # break

    print(raznica)
    # target_name: str = f'{tiker}_00_range{razmer}_splice_{year}.txt'  # Создание имени новому файлу
    # target_file: Path = Path(target_dir / target_name)  # Составление пути к новому файлу
    # result.to_csv(target_file, index=False)  # Запись в файл


if __name__ == "__main__":
    razmer: int = 250
    ticker: str = 'RTS'
    year: str = '2022'

    source_dir: Path = Path(f'c:\data_quote\data_prepare_{ticker}_range_mvc_tpsl')  # Путь к ресурсному каталогу

    # Создание списка путей к файлам
    files_path: list[Path] = list(source_dir.glob(f'*{razmer}*{year}*.txt'))

    run(files_path, razmer, year)
