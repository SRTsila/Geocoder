from building_finder import BuildingFinder
import argparse
from downloading import Downloading
import os


def input_console_data():
    """"Функция осуществляет парсинг аргументов при консольном запуске"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, help='Если хотите осуществить ввод данных через файл - используйте это')
    parser.add_argument('--make_base', type=bool,
                        help='Если нет базы данных и Вы хотите создать - введите --make_base true '
                             'если хотите создать базу данных(без неё не будет работать поиск координат)')
    parser.add_argument('--city', type=str, help='Название города')
    parser.add_argument('--street', type=str, help='Название улицы')
    parser.add_argument('--house_number', type=str, help='Номер дома')
    parser.add_argument('--download', type=bool,
                        help='Если вы хотите скачать файл с данными о России'
                             ' --download true - если ')
    namespace = parser.parse_args()
    if namespace.download is not None:
        Downloading.download_Russia_base()
        return None,
    if namespace.make_base is not None:
        path = os.path.join("./data", "Russia.osm")
        try:
            BuildingFinder.finder(path, False)
        except FileNotFoundError:
            print('загрузите базу OSM!')
        return None,
    return namespace.city, namespace.street, namespace.house_number


if __name__ == "__main__":
    data = input_console_data()
    if len(data) == 1:
        exit()
    city, street, house_number = data
    if city is None or street is None or house_number is None:
        city = input("Введите населённый пункт: ")
        street = input("Введите улицу/проспект/переулок/бульвар: ")
        house_number = input("Введите номер дома: ")
    coordinates = BuildingFinder.find_coordinates(city, street, house_number)
    try:
        result = ("Населённый пункт: {}\nУлица/проспект/переулок/бульвар: {}\nНомер дома: {}"
                  "\nДолгота: {}\nШирота: {}").format(city, street, house_number, coordinates[0], coordinates[1])
        print(result)
    except TypeError:
        pass
