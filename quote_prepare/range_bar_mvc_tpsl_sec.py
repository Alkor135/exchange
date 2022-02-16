"""
Скрипт берет файлы с рендж барами и рассчитывает положение кластера максимальных объемов
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
    for ind_file, file in enumerate(files, start=1):  # Итерация по файлам

        list_split = re.split('_', file.name, maxsplit=0)  # Разделение имени файла по '_'
        tiker = list_split[0]  # Получение тикера из имени файла
        date_quote_file = re.findall(r'\d{8}', str(file))  # Получение цифр из пути к файлу
        target_name = f'{tiker}_range{razmer}_mvc_tpsl_sec_{date_quote_file[0]}.txt'  # Создание имени новому файлу
        target_file_range: Path = Path(target_dir / target_name)  # Составление пути к новому файлу

        if Path.is_file(target_file_range):
            print(f'Файл уже существует {target_file_range}')
            continue

        df: pd = pd.read_csv(file, delimiter=',')  # Загрузка в DF range файла
        df['<SEC>'] = 0  # Создание новой колонки

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
                up = True  # Бар на повышение
                sl = low - tick  # Уровень СЛ для бара на повышение
                tp1 = high + tick + (high + tick - sl)  # Уровень ТП1 для бара на повышение
                tp2 = high + tick + (high + tick - sl) * 2   # Уровень ТП2 для бара на повышение
                tp3 = high + tick + (high + tick - sl) * 3   # Уровень ТП2 для бара на повышение
            elif close == low:  # На понижение
                up = False  # Бар на понижение
                sl = high + tick  # Уровень СЛ для бара на понижение
                tp1 = low - tick - (sl - low + tick)  # Уровень ТП1 для бара на понижение
                tp2 = low - tick - (sl - low + tick) * 2  # Уровень ТП2 для бара на понижение
                tp3 = low - tick - (sl - low + tick) * 3  # Уровень ТП3 для бара на понижение
            else:
                up = None
                continue

            df_tmp = df[row[0] + 1: len(df.index)]  # Временный DF из последующих за исследуемым баров
            for row_tmp in df_tmp.itertuples():  # Перебор последующих баров для опр. СЛ и ТП
                open_tmp = row_tmp[3]
                high_tmp = row_tmp[4]
                low_tmp = row_tmp[5]
                close_tmp = row_tmp[6]

                # Для баров на повышение
                if up and low_tmp <= sl and df.loc[row[0], '<TP_SL>'] == 0:  # SL
                    df.loc[row[0], '<TP_SL>'] = -1
                    break
                elif up and low_tmp <= sl and (df.loc[row[0], '<TP_SL>'] != 0):
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
                elif not up and high_tmp >= sl and (df.loc[row[0], '<TP_SL>'] != 0):
                    break
                elif not up and low_tmp < tp1 and df.loc[row[0], '<TP_SL>'] == 0:  # TP1
                    df.loc[row[0], '<TP_SL>'] = 1
                elif not up and low_tmp < tp2 and df.loc[row[0], '<TP_SL>'] == 1:  # TP2
                    df.loc[row[0], '<TP_SL>'] = 2
                elif not up and low_tmp < tp3 and df.loc[row[0], '<TP_SL>'] == 2:  # TP3
                    df.loc[row[0], '<TP_SL>'] = 3
                    break

            df.to_csv(target_file_range, index=False)  # Запись в файл для одного тикового файла
        # print(df)
        # break


if __name__ == "__main__":
    razmer: int = 250
    ticker: str = 'RTS'
    year: str = '2021'

    source_dir: Path = Path(f'c:\data_quote\data_prepare_{ticker}_range_mvc_tpsl')  # Путь к ресурсному каталогу
    target_dir: Path = Path(f'c:\data_quote\data_prepare_{ticker}_range_mvc_tpsl_sec')  # Путь к целевому каталогу

    if not target_dir.is_dir(): target_dir.mkdir()  # Создание каталога

    # Создание списка путей к файлам из ресурсного каталога
    files: list[Path] = [f for f in source_dir.glob(f'SPFB.RTS_range{razmer}_*_{year}*.txt')]
    print(files)

    # run(files, razmer, target_dir, tick)
