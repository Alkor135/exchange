"""
Скрипт берет файлы с рендж барами и файлы с тиками рассчитывает максимальный объем в кластере
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


def run(tick_files: list[Path], range_files: list[Path], razmer: int, target_dir: Path):

    for ind_r, range_file in enumerate(range_files, start=1):  # Итерация по range файлам

        list_split = re.split('_', range_file.name, maxsplit=0)  # Разделение имени файла по '_'
        date_quote_file = re.findall(r'\d{8}', str(range_file))  # Получение цифр из пути к файлу
        target_name = f'{list_split[0]}_{list_split[1]}_max_vol_{date_quote_file[0]}.txt'  # Создание имени новому файлу
        target_file_range: Path = Path(target_dir / target_name)  # Составление пути к новому файлу

        if Path.is_file(target_file_range):
            print(f'Файл уже существует {target_file_range}')
            continue

        df: pd = pd.read_csv(range_file, delimiter=',')  # Загрузка в DF range файла
        df['<MAX_VOLUME_PRICE>'] = None  # Создание новой колонки
        df['<MAX_VOLUME_CLUSTER>'] = None  # Создание новой колонки

        pattern_re = r'\d{8}'  # Создание паттерна для поиска тикового файла совпадающего по дате
        poisk = re.search(pattern_re, str(range_file)).group(0)  # Получение даты из имени рендж файла
        tick_file = [x for x in tick_files if poisk in str(x)]  # Выбор тикового файла по дате рендж файла
        df_tick: pd = pd.read_csv(tick_file[0], delimiter=',')  # Загрузка в DF tick файла

        # # Преобразуем столбец <TIME>, где нужно добавив 0 перед часом
        # df_tick['<TIME>'] = df_tick.apply(lambda x: zero_hour(x['<TIME>']), axis=1)

        for row_range_bar in df.itertuples():

            # Индикация прогресса
            print('\rCompleted file: {:.2f}%. Completed files: {:.2f}%'.format(
                row_range_bar[0] * 100 / len(df.index),
                ind_r * 100 / len(range_files)
                ),
                end=''
            )

            if row_range_bar[0] == len(df.index) - 1:  # Если это последняя строка range DF
                df_candle = df_tick[(df_tick['<TIME>'] >= row_range_bar[2])]
                # Группировка по ценам в свече
                s_rez = df_candle.groupby('<LAST>')['<VOL>'].sum()  # Series (в индексе цена, в значениях суммы объемов)
                max_clu = s_rez.max()  # Нахождение максимального значения в Series (макс сумма объема в кластере)
                max_idx = s_rez.idxmax()  # Нахождение индекса для максимального значения в Series (соответствует цене)

                df.loc[row_range_bar[0], '<MAX_VOLUME_PRICE>'] = max_idx  # Занесение значения цены с макс объемом в кластере
                df.loc[row_range_bar[0], '<MAX_VOLUME_CLUSTER>'] = max_clu  # Занесение значения максимального объема
            else:
                df_candle = df_tick[(df_tick['<TIME>'] >= row_range_bar[2]) &
                                    (df_tick['<TIME>'] < df.loc[(row_range_bar[0] + 1), '<TIME>'])]
                # print(df.loc[(row_range_bar[0] + 1), '<TIME>'])
                # print(df_candle)
                # Группировка по ценам в свече
                s_rez = df_candle.groupby('<LAST>')['<VOL>'].sum()  # Series (в индексе цена, в значениях суммы объемов)
                max_clu = s_rez.max()  # Нахождение максимального значения в Series (макс сумма объема в кластере)
                max_idx = s_rez.idxmax()  # Нахождение индекса для максимального значения в Series (соответствует цене)

                df.loc[row_range_bar[0], '<MAX_VOLUME_PRICE>'] = max_idx  # Занесение значения цены с макс объемом в кластере
                df.loc[row_range_bar[0], '<MAX_VOLUME_CLUSTER>'] = max_clu  # Занесение значения максимального объема

        # Изменение типа колонок
        df[['<DATE>', '<TIME>', '<VOL>']] = df[['<DATE>', '<TIME>', '<VOL>']].astype(int)
        # Преобразуем столбец <TIME>, где нужно добавив 0 перед часом
        df['<TIME>'] = df.apply(lambda x: zero_hour(x['<TIME>']), axis=1)

        df.to_csv(target_file_range, index=False)  # Запись в файла рендж баров с макс объемом

        # print(df)

        # break


if __name__ == "__main__":
    razmer: int = 250
    ticker: str = 'RTS'
    year_tick: str = '2021'

    source_dir_tick: Path = Path(f'c:/data_quote/data_finam_{ticker}_tick')  # Путь к ресурсному каталогу с тиками
    source_dir_range: Path = Path(f'c:/data_quote/data_prepare_{ticker}_range')  # Путь к ресурсному каталогу с range
    target_dir: Path = Path(f'c:/data_quote/data_prepare_{ticker}_range_max_vol')  # Путь к целевому каталогу

    if not target_dir.is_dir(): target_dir.mkdir()  # Создание каталога

    tick_files: list[Path] = list(source_dir_tick.glob(f'*{year_tick}*.csv'))  # Создание списка путей к файлам с тиками
    range_files: list[Path] = list(source_dir_range.glob(f'*{year_tick}*.txt'))  # Создание списка путей к файлам с range
    range_files = [x for x in range_files if f'{razmer}' in str(x)]  # Фильтрация списка по размеру ренджа

    run(tick_files, range_files, razmer, target_dir)
