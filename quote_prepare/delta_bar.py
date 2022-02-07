"""
Скрипт из файлов с тиковыми данными делает файл с дельта барами
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


def run(tick_files: list, delta_max_val: int, target_dir: Path):

    for ind_file, tick_file in enumerate(tick_files, start=1):  # Итерация по файлам

        list_split = re.split('_', tick_file.name, maxsplit=0)  # Разделение имени файла по '_'
        tiker = list_split[0]  # Получение тикера из имени файла
        date_quote_file = re.findall(r'\d+', str(tick_file))  # Получение цифр из пути к файлу
        target_name = f'{tiker}_delta_{date_quote_file[0]}.csv'  # Создание имени новому файлу
        target_file_delta: Path = Path(target_dir / target_name)  # Составление пути к файлу

        if Path.is_file(target_file_delta):  # Если файл существует
            print(f'Файл уже существует {target_file_delta}')
            continue
        else:
            df_ticks_file: pd = pd.read_csv(tick_file, delimiter=',')  # Считываем тиковые данные в DF
            previous_tick = 0
            direction_tick_up = True

            # Создание DF под дельта бары одного тикового файла
            df: pd = pd.DataFrame(columns='<DATE> <TIME> <OPEN> <HIGH> <LOW> <CLOSE> <VOL> <DELTA>'.split(' '))

            for tick in df_ticks_file.itertuples():  # Итерация по строкам тикового DF
                print('\rCompleted file: {:.2f}%. Completed files: {:.2f}%'.format(
                    tick[0] * 100 / len(df_ticks_file.index),
                    ind_file * 100 / len(tick_files)
                    ),
                    end=''
                )

                if tick[0] == 0:
                    # Добавление строки в DF с дельта барами
                    df.loc[len(df.index)] = [int(tick[1]), int(tick[2]), tick[3], tick[3], tick[3], tick[3], tick[4], 0]

                # Если бар сформирован по дельте и время открытия бара меньше времени текущего тика (защита от быстрого рынка)
                elif abs(df.iloc[-1]['<DELTA>']) >= delta_max_val and df.iloc[-1]['<TIME>'] < tick[2]:
                    # Добавление строки в DF с дельта барами
                    df.loc[len(df.index)] = [int(tick[1]), int(tick[2]), tick[3], tick[3], tick[3], tick[3], tick[4], 0]

                # Заполняем(изменяем) последнюю строку DF с дельта баром --------------------------------------
                # Записываем <CLOSE> --------------------------------------------------------------------------
                df.loc[len(df) - 1, '<CLOSE>'] = tick[3]  # Записываем последнюю цену как цену close бара

                # Записываем <HIGH> ---------------------------------------------------------------------------
                if float(tick[3]) > df.loc[len(df) - 1, '<HIGH>']:  # Если цена последнего тика больше чем high
                    df.loc[len(df) - 1, '<HIGH>'] = tick[3]  # Записываем цену последнего тика как high

                # Записываем <LOW> ----------------------------------------------------------------------------
                if float(tick[3]) < df.loc[len(df) - 1, '<LOW>']:
                    df.loc[len(df) - 1, '<LOW>'] = tick[3]  # Записываем цену последней сделки как low

                # Записываем <VOL> ----------------------------------------------------------------------------
                df.loc[len(df) - 1, '<VOL>'] += tick[4]  # Увеличиваем объем

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

            # Изменение типа колонок
            df[['<DATE>', '<TIME>', '<VOL>', '<DELTA>']] = df[['<DATE>', '<TIME>', '<VOL>', '<DELTA>']].astype(int)
            # Преобразуем столбец <TIME>, где нужно добавив 0 перед часом
            df['<TIME>'] = df.apply(lambda x: zero_hour(x['<TIME>']), axis=1)

            df.to_csv(target_file_delta, index=False)  # Запись в файл для одного тикового файла
            df = df.iloc[0:0]

        # break  # Прерывание загрузки следующего файла
    # df.to_csv(target_file_delta, index=False)  # Запись в файл для всего массива


if __name__ == "__main__":
    ticker: str = 'RTS'
    year_tick: str = '2022'
    delta_max_val: int = 500
    source_dir_tick: Path = Path(f'c:/data_quote/data_finam_{ticker}_tick')  # Путь к ресурсному каталогу
    target_dir: Path = Path(f'c:/data_quote/data_prepare_{ticker}_delta')  # Путь к целевому каталогу

    # Создание списка путей к файлам с тиками
    tick_files: list[Path] = list(source_dir_tick.glob(f'*{year_tick}*.csv'))

    run(tick_files, delta_max_val, target_dir)
