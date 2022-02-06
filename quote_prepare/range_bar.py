"""
Скрипт из файлов с тиковыми данными делает файл с рандже барами
"""
import re
from datetime import datetime
from pathlib import *

import pandas as pd


def zero_hour(cell):
    """ Функция преобразует время (с финама приходят часы без нулей (с декабря 2021), которые pandas не воспринимает)"""
    cell = f'{int(cell)}'
    tmp_time = datetime.strptime(cell, "%H%M%S")
    return tmp_time.strftime("%H%M%S")


def run(tick_files: list[Path], razmer: int, target_dir: Path):

    for ind_file, tick_file in enumerate(tick_files, start=1):  # Итерация по тиковым файлам

        list_split = re.split('_', tick_file.name, maxsplit=0)  # Разделение имени файла по '_'
        tiker = list_split[0]  # Получение тикера из имени файла
        date_quote_file = re.findall(r'\d+', str(tick_file))  # Получение цифр из пути к файлу
        target_name = f'{tiker}_range{razmer}_{date_quote_file[0]}.txt'  # Создание имени новому файлу
        target_file_range: Path = Path(target_dir / target_name)  # Составление пути к файлу

        if Path.is_file(target_file_range):
            print(f'Файл уже существует {target_file_range}')
            continue
        else:
            df_ticks_file: pd = pd.read_csv(tick_file, delimiter=',')  # Считываем тиковые данные в DF

            # Создание DF под рандже бары одного тикового файла
            df: pd = pd.DataFrame(columns='<DATE> <TIME> <OPEN> <HIGH> <LOW> <CLOSE> <VOL>'.split(' '))

            for tick in df_ticks_file.itertuples():  # Итерация по строкам тикового DF
                print('\rCompleted file: {:.2f}%. Completed files: {:.2f}%'.format(
                    tick[0] * 100 / len(df_ticks_file.index),
                    ind_file * 100 / len(tick_files)
                    ),
                    end=''
                )

                if tick[0] == 0:
                    # Добавление строки в DF с рандже барами
                    df.loc[len(df.index)] = [int(tick[1]), int(tick[2]), tick[3], tick[3], tick[3], tick[3], tick[4]]
                    continue

                # Если бар сформирован по размеру возрастающий бар
                if df.loc[len(df.index) - 1, '<LOW>'] + razmer < tick[3]:
                    df.loc[len(df.index) - 1, '<CLOSE>'] = df.loc[len(df.index) - 1, '<LOW>'] + razmer
                    df.loc[len(df.index) - 1, '<HIGH>'] = df.loc[len(df.index) - 1, '<CLOSE>']
                    # Добавление строки в DF с дельта барами
                    df.loc[len(df.index)] = [int(tick[1]), int(tick[2]), tick[3], tick[3], tick[3], tick[3], tick[4]]
                    continue
                    # break

                # Если бар сформирован по размеру падающий бар
                if df.loc[len(df) - 1, '<HIGH>'] - razmer > tick[3]:
                    df.loc[len(df) - 1, '<CLOSE>'] = df.loc[len(df) - 1, '<HIGH>'] - razmer
                    df.loc[len(df) - 1, '<LOW>'] = df.loc[len(df) - 1, '<CLOSE>']
                    # Добавление строки в DF с дельта барами
                    df.loc[len(df.index)] = [int(tick[1]), int(tick[2]), tick[3], tick[3], tick[3], tick[3], tick[4]]
                    continue
                    # break

                # Заполняем(изменяем) последнюю строку DF с рандже баром --------------------------------------
                # Записываем <CLOSE> --------------------------------------------------------------------------
                df.loc[len(df.index) - 1, '<CLOSE>'] = tick[3]  # Записываем последнюю цену как цену close бара

                # Записываем <HIGH> ---------------------------------------------------------------------------
                if float(tick[3]) > df.loc[len(df) - 1, '<HIGH>']:  # Если цена последнего тика больше чем high
                    df.loc[len(df.index) - 1, '<HIGH>'] = tick[3]  # Записываем цену последнего тика как high

                # Записываем <LOW> ----------------------------------------------------------------------------
                if float(tick[3]) < df.loc[len(df.index) - 1, '<LOW>']:
                    df.loc[len(df.index) - 1, '<LOW>'] = tick[3]  # Записываем цену последней сделки как low

                # Записываем <VOL> ----------------------------------------------------------------------------
                df.loc[len(df.index) - 1, '<VOL>'] += tick[4]  # Увеличиваем объем

            # Изменение типа колонок
            df[['<DATE>', '<TIME>', '<VOL>']] = df[['<DATE>', '<TIME>', '<VOL>']].astype(int)
            # Преобразуем столбец <TIME>, где нужно добавив 0 перед часом
            df['<TIME>'] = df.apply(lambda x: zero_hour(x['<TIME>']), axis=1)

            df.to_csv(target_file_range, index=False)  # Запись в файл для одного тикового файла

        # break


if __name__ == "__main__":
    razmer: int = 250
    ticker: str = 'RTS'
    year_tick: str = '2022'

    source_dir_tick: Path = Path(f'c:/data_quote/data_finam_{ticker}_tick')  # Путь к ресурсному каталогу
    target_dir: Path = Path(f'c:/data_quote/data_prepare_{ticker}_range')  # Путь к целевому каталогу

    # Создание списка путей к файлам с тиками
    tick_files: list[Path] = list(source_dir_tick.glob(f'*{year_tick}*.csv'))

    run(tick_files, razmer, target_dir)
