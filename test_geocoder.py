from geometry import Geometry
import unittest
import numpy
from building import Building
from building_finder import BuildingFinder


class GeometryTest(unittest.TestCase):
    def test_centroid_finder(self):
        coordinates = numpy.array([[10, 10], [20, 20], [10, 20], [20, 10]])
        result = [10.0, 3.333333333333332]
        self.assertEqual(result, list(Geometry.find_centroid(coordinates, len(coordinates))))

    def test_create_building(self):
        data = ("Екатеринбрг", "улица Тургенева", "4", [])
        build = Building(address=data[1], house_number=data[2], references=data[3], city=data[0])
        self.assertEqual(("Екатеринбрг", "Тургенева", "4"), (build.city, build.address, build.house_number))

    def test_addresses_finder(self):
        BuildingFinder.finder("./data/test_data.txt", True)
        self.assertEqual([56.78143291012384, 60.87707735411823],
                         BuildingFinder.find_coordinates("Исток", "Главная", "24А", True))
