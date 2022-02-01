"""
Подготовка данных 5 минутных котировок.
Берется файл с 5мин данными и файлы с тиковыми данными.
Из тиковых данных расcчитывается кластер с максимальными объемами и дописывается столбцом к 5мин данным.
Полученный массив данных сохраняется в новый файл, для последующего анализа и построения графиков.
"""
import pandas as pd
from pathlib import *

source_file_5m: Path = Path('c:\data_quote\data_finam_RTS_5m\SPFB.RTS_2020.csv')
source_dir_tick: Path = Path('c:\data_quote\data_finam_RTS_tick')
target_file_5m: Path = Path('c:\data_quote\data_prepare_RTS_5m\SPFB.RTS_2020.csv')
year_tick = '2020'


pd.set_option('max_rows', 5)  # Установка 5 строк вывода DF
pd.set_option('display.max_columns', None)  # Сброс ограничений на число столбцов
# Создание df для 5 мин баров
df_5m: pd = pd.read_csv(source_file_5m, delimiter=',')
df_5m['<MAX_VOLUME_PRICE>'] = None  # Создание новой колонки
df_5m['<MAX_VOLUME_CLUSTER>'] = None  # Создание новой колонки

# Создание списка путей к файлам с тиками
tick_files: list[Path] = list(source_dir_tick.glob(f'*{year_tick}*.csv'))

# Создание DF под тики
df_tick: pd = pd.DataFrame

for row_5m in df_5m.itertuples():
    date_candle: int = row_5m[1]  # Дата начала выбранной свечи (int прочитано из файла)
    time_candle: int = row_5m[2]  # Время начала выбранной свечи (int прочитано из файла)
    # print(f'{date_candle=}, {time_candle=}')

    # Если тиковый DF пустой или дата 5мин свечи не совпадает с тиковой датой
    if df_tick.empty or int(date_candle) != int(df_tick.iloc[0, 0]):
        # print(f'{date_candle=}, {time_candle=}')
        # Выбор подходящего по дате файла
        tick_file: list[tuple] = [(i, file) for i, file in enumerate(tick_files) if str(row_5m[1]) in str(file)]
        if len(tick_file) > 0:  # Если файл с подходящей датой найден
            df_tick = pd.read_csv(Path(tick_file[0][1]), delimiter=',')  # Считываем тиковые данные в DF
            print('\rCompleted: {:.2f}%'.format(tick_file[0][0]*100/len(tick_files)), end='')

    # Формирование тикового DF под 5мин свечу
    df_candle = df_tick[(df_tick['<TIME>'] >= time_candle) & (df_tick['<TIME>'] < time_candle + 500)]

    # Группировка по ценам в свече
    s_rez = df_candle.groupby('<LAST>')['<VOL>'].sum()  # Series (в индексе цена, в значениях суммы объемов)
    max_clu = s_rez.max()  # Нахождение максимального значения в Series (макс сумма объема в кластере)
    max_idx = s_rez.idxmax()  # Нахождение индекса для максимального значения в Series (соответствует цене)

    df_5m.loc[row_5m[0], '<MAX_VOLUME_PRICE>'] = max_idx  # Занесение значения цены с макс объемом в кластере
    df_5m.loc[row_5m[0], '<MAX_VOLUME_CLUSTER>'] = max_clu  # Занесение значения максимального объема

# Пишем в файл результат (без индекса)
df_5m.to_csv(target_file_5m, index=False)
print(df_5m)
