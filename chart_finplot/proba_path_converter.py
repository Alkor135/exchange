"""
Проба выделить часть имени файла
"""
from pathlib import *
import re


if __name__ == "__main__":
    ticker: str = 'RTS'
    year_tick: str = '2021'
    delta_max_val: int = 500
    source_dir_tick: Path = Path(f'c:/data_quote/data_finam_{ticker}_tick')  # Ресурсный каталог

    # Создание списка путей к файлам с тиками
    tick_files: list[Path] = list(source_dir_tick.glob(f'*{year_tick}*.csv'))

    print(tick_files)
    for file in tick_files:
        # print(str(file))  # Полный путь к файлу
        # print(file.name)  # Имя файла
        # print(type(file.name))  # Тип имени файла str
        # print(file.parent)  # Директория файла
        #
        # num = re.findall(r'\d+', str(file))  # Получение цифр из пути к файлу
        # print(num[0])

        list_split = re.split('_', file.name, maxsplit=0)  # Разделение имени файла по '_'
        tiker = list_split[0]  # Получение тикера из имени файла
        date_quote_file = re.findall(r'\d+', str(file))  # Получение цифр из пути к файлу
        print(f'{tiker}_{date_quote_file[0]}')

        # Проверка на существование файла
        file_name = file.name
        path_dir = file.parent
        if Path.is_file(path_dir / file_name):
            print(f'Файл уже существует {Path(path_dir / file_name)}')

        # urezannoe_name_file = re.search('.*?', file.name)
        # print(urezannoe_name_file)
