"""
Линейная регрессия
"""
from pathlib import *
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.metrics import r2_score


def zero_hour(cell):
    """ Функция преобразует время (с финама приходят часы без нулей (с марта 2021), которые pandas не воспринимает)"""
    cell = f'{int(cell)}'
    tmp_time = datetime.strptime(cell, "%H%M%S")
    return tmp_time.strftime("%H%M%S")


def change_tp(cell, tp: int):
    """ Преобразует значение ТП в зависимости от выбора"""
    if tp == 1:
        if cell in [2, 3]:
            return 1
        else:
            return cell
    elif tp == 2:
        if cell == 3:
            return 2
        elif cell == 1:
            return -1
        else:
            return cell
    elif tp == 3:
        if cell in [1, 2]:
            return -1
        else:
            return cell
    else:
        return cell


def stat_sec(df: pd, start_sec: int, end_sec: int):
    for i in range(start_sec, end_sec + 1):
        df_prn = df.copy()
        df_prn = df_prn.loc[df_prn['<SEC>'] <= i]  # Выборка под заданное время формирования бара
        print(f'\n{start_sec}-{i}\n{df_prn["<TP_SL>"].value_counts()}')
        print(f'{start_sec}-{i}\n{df_prn["<TP_SL>"].value_counts(normalize=True)}')


if __name__ == "__main__":
    TP = 1
    start_sec = 7
    end_sec = 60
    # Загружаем файл в DF
    df = pd.read_csv(
        Path('c:\data_quote\data_prepare_RTS_range_mvc_tpsl_sec\SPFB.RTS_00_range250_splice_2022.txt'),
        delimiter=','
    )

    # Настройки отображения DF
    pd.set_option('max_rows', 5)  # Установка 5 строк вывода DF
    pd.set_option('display.max_columns', None)  # Сброс ограничений на число столбцов

    # Обработка DF
    df['<TIME>'] = df.apply(lambda x: zero_hour(x['<TIME>']), axis=1)  # Преобразуем столбец <TIME>, где нужно добавив 0 перед часом
    df['<DATE_TIME>'] = df['<DATE>'].astype(str) + ' ' + df['<TIME>'].astype(str)  # Создаем новый столбец <DATE_TIME> слиянием столбцов <DATE> и <TIME>
    df = df.set_index(pd.DatetimeIndex(df['<DATE_TIME>']))  # Меняем индекс и делаем его типом datetime
    df.drop(labels=['<DATE_TIME>', '<DATE>', '<TIME>', '<VOL>'], axis=1, inplace=True)  # Удаляем ненужные колонки. axis=1 означает, что отбрасываем колонку а не индекс
    df = df.loc[df['<TP_SL>'] != 0]  # Убираем строки где <TP_SL> равен 0
    df = df.loc[df['<HIGH>'] > df['<MAX_VOLUME_PRICE>']]
    df = df.loc[df['<MAX_VOLUME_PRICE>'] > df['<LOW>']]

    df['<TP_SL>'] = df.apply(lambda x: change_tp(x['<TP_SL>'], TP), axis=1)  # Преобразование под ТП
    print(f'{df["<TP_SL>"].value_counts()}')
    print(f'{df["<TP_SL>"].value_counts(normalize=True)}')

    # stat_sec(df, start_sec, end_sec)

    Xtrain = df['<TP_SL>'].values
    Ytrain = df['<SEC>'].values
    plt.scatter(Xtrain, Ytrain, color='red')

    regr = linear_model.LinearRegression()
    Xtrain = Xtrain.reshape(len(Xtrain), 1)
    Ytrain = Ytrain.reshape(len(Ytrain), 1)

    regr.fit(Xtrain, Ytrain)
    Ypredicted = regr.predict(Xtrain)

    plt.plot(Xtrain, Ypredicted)
    r2_easy = r2_score(Ytrain, Ypredicted)

    print(r2_easy)

    # X = df['<TP_SL>']
    # Y = df['<SEC>']
    # plt.scatter(X, Y)
    plt.show()

    # print(df)
