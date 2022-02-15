"""
После запуска сервера(этого скрипта), в КВИКе запускаем луа-скрипт QuikLuaPython_3599_TCP.lua
Данные от сервера в обработчик передаются по средствам организации очереди Queue
Сервер останавливается, когда клиент закрывает соединение
"""
import socket
import threading
from datetime import datetime, timezone
from multiprocessing import Queue
import finplot as fplt
import pandas as pd
import winsound


def parser():
    while True:
        parse = queue.get()  # Получаем из очереди данные от клиента
        print(f'Парсер {parse}')


def service():
    """
    TCP сокет-сервер на порту 3599 с постоянным прослушиванием. Клиент подсоединяется один раз и передает
    данные когда угодно. От клиента приходят строки, разделенные символом \n, информация в строках разделена пробелами
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 3599))  # Запускаем сервер на локальной машине, порт 3599
    s.listen(5)  # Начинаем прослушивать (до 5 соединений)
    # Принимаем соединения с помощью функции accept. Она ждёт появления входящего соединения и
    # возвращает связанный с ним сокет и адрес подключившегося. Адрес — массив, состоящий из IP-адреса и порта.
    conn, addr = s.accept()
    global client
    client = conn
    tail = b''  # Не уместившееся полностью в буфер сообщение от клиента. В начале - пустая строка.
    while True:  # "вечный" цикл, пока клиент не "отвалится"
        data = conn.recv(1024)  # Принимаем в буфер data(1024 байт) сообщения от клиента
        if not data:  # Если клиент закрыл сокет,
            conn.close()  # то сервер закрывает это соединение и выходит из цикла
            break
        else:
            # Хотя клиент и отсылает сообщения по одному, разделяя их символом \n, но если идет большой поток сообщений
            # в цикле, то в буфер могут попасть несколько сообщений одновременно
            messages = data.splitlines()  # по-этому, разделяем сообщения в буфере на строки
            # Если на момент обработки буфера присутствует "хвост" от прошлого сообщения
            # (т.е. оно не уместилось целиком в буфере),
            messages[0] = tail + messages[0]  # добавляем его в начало первого сообщения в буфере
            # Если последним элементом в буфере является символ новой строки \n, то все сообщения уместились в буфере
            if data[-1] == 10:  # 10 - это байт-код символа новой строки \n
                tail = b''  # В этом случае "хвостов" не осталось
            else:  # а если сообщение не уместилось в буфер,
                tail = messages[-1]  # то сохраняем этот кусок(последний элемент) как tail
                messages = messages[:-1]  # а сами сообщения сохраняем, но без последнего "обрезка"
            # С этого места можно обрабатывать список сообщений от клиента с гарантией,
            # что все сообщения целы и не обрезаны буфером
            # print('Clear:', messages)
            for message in messages:
                message = message.decode()  # переводим из бинарной кодировки в utf8
                # print(f'utf-8 кодировка {message}')
                message = message.split(' ')
                # if message[0] == '1' and message[1] == ticker:
                # if message[0] == '2':
                if message[0] == '1':
                    print(f'Помещаем в очередь {message}')
                    queue.put(message)  # Помещаем в очередь данные от клиента

    conn.close()  # если клиент закрыл соединение то и мы закрываем соединение
    s.close()


if __name__ == '__main__':
    # Изменяемые настройки
    ticker = 'RIH2'
    range_size = 250

    client = None
    fplt.display_timezone = timezone.utc  # Настройка тайм зоны, чтобы не было смещения времени

    # Настройки для отображения широкого df pandas
    pd.options.display.width = 1200
    pd.options.display.max_colwidth = 100
    pd.options.display.max_columns = 100

    # delta_bars = DeltaBars()  # Создаем экземпляр класса DeltaBar
    queue = Queue()  # Создаем очередь
    # Запускаем сервер в своем потоке
    print('Info: Запуск клиента нужно производить после запуска сервера!')
    t = threading.Thread(name='service', target=service)
    t.start()

    # Запускаем парсер в своем потоке
    t_parser = threading.Thread(name='parser', target=parser)
    t_parser.start()

    # plots = []
    # ax, ax2, ax3 = fplt.create_plot(ticker, init_zoom_periods=100, maximize=False, rows=3)
    # ax.set_visible(xgrid=True, ygrid=True)
    # ax2.set_visible(xgrid=True, ygrid=True)
    # update()
    # fplt.timer_callback(update, 2.0)  # update (using synchronous rest call) every N seconds
    #
    # fplt.show()
