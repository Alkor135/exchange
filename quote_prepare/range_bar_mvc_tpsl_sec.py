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


def run(files: list[Path], razmer: int, target_dir: Path):
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
        df['<SEC>'] = 900  # Создание новой колонки под время формирования бара
        df['<PER>'] = 2  # Создание новой колонки под процент макс объема
        # print(df)
        # print(len(df.index))
        # break

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
            cluster = row[8]

            if (high - low) > 0:
                if close == high:  # На повышение
                    df.loc[row[0], '<PER>'] = (cluster - low) / (high - low)
                elif close == low:  # На понижение
                    df.loc[row[0], '<PER>'] = (high - cluster) / (high - low)

            if row[0] != len(df.index) - 1:  # Если это не последняя строка
                current_dt = f"{df.loc[row[0], '<DATE>']} {df.loc[row[0], '<TIME>']}"  # Время откр. текущего бара
                current_dt = datetime.strptime(current_dt, '%Y%m%d %H%M%S')

                next_dt = f"{df.loc[row[0]+1, '<DATE>']} {df.loc[row[0]+1, '<TIME>']}"  # Время откр. следующего бара
                next_dt = datetime.strptime(next_dt, '%Y%m%d %H%M%S')

                df.loc[row[0], '<SEC>'] = int((next_dt - current_dt).total_seconds())  # Запись секунд


                df.to_csv(target_file_range, index=False)  # Запись в файл для одного тикового файла
        # print(df)
        # break


if __name__ == "__main__":
    razmer: int = 250
    ticker: str = 'RTS'
    year: str = '2022'

    # Настройки отображения DF
    pd.set_option('max_rows', 5)  # Установка 5 строк вывода DF
    pd.set_option('display.max_columns', None)  # Сброс ограничений на число столбцов

    source_dir: Path = Path(f'c:\data_quote\data_prepare_{ticker}_range_mvc_tpsl')  # Путь к ресурсному каталогу
    target_dir: Path = Path(f'c:\data_quote\data_prepare_{ticker}_range_mvc_tpsl_sec')  # Путь к целевому каталогу

    if not target_dir.is_dir(): target_dir.mkdir()  # Создание каталога

    # Создание списка путей к файлам из ресурсного каталога
    files: list[Path] = [f for f in source_dir.glob(f'SPFB.RTS_range{razmer}_*_{year}*.txt')]
    print(files)

    run(files, razmer, target_dir)
