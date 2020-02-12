import re
from building import Building
from geometry import Geometry
import numpy
import sqlite3
import os


class BuildingFinder:

    @staticmethod
    def finder(file_name, test):
        """"Функция составляет базу данных из OSM-кого формата"""
        try:
            if not test:
                coord_path = os.path.join("./test_base", "Russia_coordinates.db")
                buildings_path = os.path.join("./test_base", "Russia_buildings.db")
            else:
                coord_path = os.path.join("./test_base", "test_coordinates.db")
                buildings_path = os.path.join("./test_base", "test_buildings.db")
            con1 = sqlite3.connect(coord_path)
            cur1 = con1.cursor()
            cur1.execute('CREATE TABLE IF NOT EXISTS coordinates_base(Link INTEGER, Lat REAL, Lon REAL)')
            con2 = sqlite3.connect(buildings_path)
            cur2 = con2.cursor()
            cur2.execute('CREATE TABLE IF NOT EXISTS address_base(City TEXT,Address TEXT,House_number TEXT,Links TEXT)')
            with open(file_name, encoding='utf-8') as f:
                buffer = []
                counter = 0
                current_city = ""
                for string in f:
                    string = string.lstrip()[:-1]
                    buffer.append(string)
                    if counter <= 0:
                        if re.match(r'<node id="', string) is not None:
                            try:
                                s = re.findall(r'[0-9]{2}.[0-9]+', string)
                                coordinates = ([int(s[0]), float(s[4]), float(s[5])])
                                cur1.execute("INSERT INTO coordinates_base VALUES(?,?,?)", coordinates)
                            except IndexError:
                                continue
                        if re.match(r'<tag k="addr:street" v="', string) is not None:
                            j = 0
                            is_house = False
                            for j in range(len(buffer) - 1, -1, -1):
                                if re.match(r'<way id="', buffer[j]) is not None:
                                    is_house = True
                                    break
                            if is_house:
                                references = []
                                street = string[24:-3]
                                house_number = None
                                city = current_city
                                for i in range(j, len(buffer)):
                                    if re.match(r'<tag k="addr:housenumber" v=', buffer[i]) is not None:
                                        house_number = buffer[i][29:-3]
                                        continue
                                    if re.match(r'<tag k="addr:city" v=', buffer[i]) is not None:
                                        city = buffer[i][22:-3].capitalize()
                                        current_city = city
                                    if re.match(r'<nd ref="', buffer[i]) is not None:
                                        references.append(buffer[i][9:-3])
                                if house_number is not None:
                                    build = Building(street, house_number, references, city)
                                    references = " ".join(build.references)
                                    cur2.execute("INSERT INTO address_base VALUES(?,?,?,?)",
                                                 [build.city, build.address, build.house_number, references])
                                elif house_number is None:
                                    counter = 5
                    elif counter > 0:
                        counter -= 1
                        if re.match(r'<tag k="addr:housenumber" v=', string) is not None:
                            counter = 0
                            j = 0
                            is_house = False
                            for j in range(len(buffer) - 1, -1, -1):
                                if re.match(r'<way id="', buffer[j]) is not None:
                                    is_house = True
                                    break
                            if is_house:
                                references = []
                                house_number = string[29:-3]
                                city = current_city
                                street = None
                                for i in range(j, len(buffer)):
                                    if re.match(r'<tag k="addr:street"', buffer[i]) is not None:
                                        street = buffer[i][24:-3]
                                        continue
                                    if re.match(r'<nd ref="', buffer[i]) is not None:
                                        references.append(buffer[i][9:-3])
                                    if re.match(r'<tag k="addr:city" v=', buffer[i]) is not None:
                                        city = buffer[i][22:-3].capitalize()
                                        current_city = city
                                if street is not None:
                                    build = Building(street, house_number, references, city)
                                    references = " ".join(build.references)
                                    cur2.execute("INSERT INTO address_base VALUES(?,?,?,?)",
                                                 [build.city, build.address, build.house_number, references])
                    if len(buffer) == 40:
                        buffer.pop(0)
            con1.commit()
            con2.commit()
        except FileNotFoundError:
            raise FileNotFoundError("База OSM не загружена!")

    @staticmethod
    def find_coordinates(city, address, number_of_house, test=False):
        """Функция ищет координаты по задонному адресу"""
        coordinates = []
        try:
            if not test:
                coordinate_path = os.path.join("./test_base", "Russia_coordinates.db")
                buildings_path = os.path.join("./test_base", "Russia_buildings.db")
            else:
                coordinate_path = os.path.join("./test_base", "test_coordinates.db")
                buildings_path = os.path.join("./test_base", "test_buildings.db")
            con1 = sqlite3.connect(coordinate_path)
            cur1 = con1.cursor()
            con2 = sqlite3.connect(buildings_path)
            cur2 = con2.cursor()
            sql = "SELECT Links FROM address_base WHERE City=? AND Address=? AND House_number=?"
            cur2.execute(sql, [city, address, number_of_house])
            links = cur2.fetchone()[0]
            links = links.split()
            res = []
            for link in links:
                res.append(int(link))
            for i in res:
                sql2 = "SELECT Lat,Lon FROM coordinates_base WHERE Link=?"
                cur1.execute(sql2, [i])
                c = cur1.fetchall()
                coordinates.append([c[0][0], c[0][1]])
            coordinates = numpy.array(coordinates)
            return Geometry.find_centroid(coordinates, len(coordinates))
        except TypeError:
            print('Нет такого адреса в базе: {}'.format(str.join(" ", [city, address, number_of_house])))
