"""
Скрипт берет файлы с рендж барами и обсчитывает SL и TP
SL на один тик ниже/выше бара расчета
TP равен выше/ниже 1/2/3 SL
"""
import re
from datetime import datetime
from pathlib import *

import pandas as pd


def zero_hour(cell):
    """ Функция преобразует время (с финама приходят часы без нулей (с марта 2021), которые pandas не воспринимает)"""
    cell = f'{int(cell)}'
    tmp_time = datetime.strptime(cell, "%H%M%S")
    return tmp_time.strftime("%H%M%S")


def run(files: list[Path], razmer: int, target_dir: Path, tick: int):
    print(files)
    for ind_file, file in enumerate(files, start=1):  # Итерация по файлам
        print('for')

        list_split = re.split('_', file.name, maxsplit=0)  # Разделение имени файла по '_'
        tiker = list_split[0]  # Получение тикера из имени файла
        date_quote_file = re.findall(r'\d{8}', str(file))  # Получение цифр из пути к файлу
        target_name = f'{tiker}_range{razmer}_mvc_tpsl_{date_quote_file[0]}.txt'  # Создание имени новому файлу
        target_file_range: Path = Path(target_dir / target_name)  # Составление пути к новому файлу

        if Path.is_file(target_file_range):
            print(f'Файл уже существует {target_file_range}')
            continue

        df: pd = pd.read_csv(file, delimiter=',')  # Загрузка в DF range файла
        df['<TP_SL>'] = 0  # Создание новой колонки

        for row in df.itertuples():
            # Индикация прогресса
            print('\rCompleted file: {:.2f}%. Completed files: {:.2f}%'.format(
                row[0] * 100 / len(df.index),
                ind_file * 100 / len(files)
                ),
                end=''
            )

            open = row[3]
            high = row[4]
            low = row[5]
            close = row[6]
            up = None
            rez = 0

            if close == high:  # На повышение
                up = True
                sl = low - tick
                tp1 = high + tick + (high + tick - sl)
                tp2 = high + tick + (high + tick - sl) * 2
                tp3 = high + tick + (high + tick - sl) * 3
            elif close == low:  # На понижение
                up = False
                sl = high + tick
                tp1 = low - tick - (sl - low + tick)
                tp2 = low - tick - (sl - low + tick) * 2
                tp3 = low - tick - (sl - low + tick) * 3
            else:
                up = None
                continue
            # print(f'   {sl=} {tp1=} {tp2=} {tp3=}')

            df_tmp = df[row[0] + 1: len(df.index)]
            # print(df_tmp)
            for row_tmp in df_tmp.itertuples():
                open_tmp = row_tmp[3]
                high_tmp = row_tmp[4]
                low_tmp = row_tmp[5]
                close_tmp = row_tmp[6]

                # Для баров на повышение
                if up and low_tmp <= sl and df.loc[row[0], '<TP_SL>'] == 0:  # SL
                    df.loc[row[0], '<TP_SL>'] = -1
                    break
                elif up and low_tmp <= sl and (df.loc[row[0], '<TP_SL>'] == 1 or  # End TP
                                               df.loc[row[0], '<TP_SL>'] == 2 or
                                               df.loc[row[0], '<TP_SL>'] == 3):
                    break
                elif up and high_tmp > tp1 and df.loc[row[0], '<TP_SL>'] == 0:  # TP1
                    df.loc[row[0], '<TP_SL>'] = 1
                elif up and high_tmp > tp2 and df.loc[row[0], '<TP_SL>'] == 1:  # TP2
                    df.loc[row[0], '<TP_SL>'] = 2
                elif up and high_tmp > tp3 and df.loc[row[0], '<TP_SL>'] == 2:  # TP3
                    df.loc[row[0], '<TP_SL>'] = 3
                    break

                # Для баров на понижение
                if not up and high_tmp >= sl and df.loc[row[0], '<TP_SL>'] == 0:  # SL
                    df.loc[row[0], '<TP_SL>'] = -1
                    break
                elif not up and high_tmp >= sl and (df.loc[row[0], '<TP_SL>'] == 1 or  # End TP
                                                    df.loc[row[0], '<TP_SL>'] == 2 or
                                                    df.loc[row[0], '<TP_SL>'] == 3):
                    break
                elif not up and low_tmp < tp1 and df.loc[row[0], '<TP_SL>'] == 0:  # TP1
                    df.loc[row[0], '<TP_SL>'] = 1
                elif not up and low_tmp < tp1 and df.loc[row[0], '<TP_SL>'] == 1:  # TP2
                    df.loc[row[0], '<TP_SL>'] = 2
                elif not up and low_tmp < tp1 and df.loc[row[0], '<TP_SL>'] == 2:  # TP3
                    df.loc[row[0], '<TP_SL>'] = 3
                    break
        print(df)
        break


if __name__ == "__main__":
    razmer: int = 250
    ticker: str = 'RTS'
    year: str = '2021'
    tick: int = 10

    source_dir: Path = Path(f'c:\data_quote\data_prepare_{ticker}_range_max_vol')  # Путь к ресурсному каталогу
    target_dir: Path = Path(f'c:\data_quote\data_prepare_{ticker}_range_mvc_tpsl')  # Путь к целевому каталогу

    if not target_dir.is_dir(): target_dir.mkdir()  # Создание каталога

    # Создание списка путей к файлам из ресурсного каталога
    files: list[Path] = [f for f in source_dir.glob(f'SPFB.RTS_range{razmer}_max_vol_{year}*.txt')]

    run(files, razmer, target_dir, tick)
