from main import *
import unittest
import os

class TestRouteCostProgram(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_passenger_data = [
    {
        "name": "ім'я1 прізвище1 по-батькові1",
        "from": "місто1",
        "to": "місто14"
    },
    {
        "name": "ім'я2 прізвище2 по-батькові2",
        "from": "місто2",
        "to": "місто10"
    },
    {
        "name": "ім'я3 прізвище3 по-батькові3",
        "from": "місто3",
        "to": "місто2"
    }
]
        cls.mock_routes_data = [
    {
        "from": "місто1",
        "to": "місто14",
        "dist": 1317
    },
    {
        "from": "місто2",
        "to": "місто10",
        "dist": 1423
    },
    {
        "from": "місто3",
        "to": "місто2",
        "dist": 1000
    }
]
        cls.routeCost = RouteCost("data/_passengers.json", "data/_routes.json", 10)

    def setUp(self):
        restore_json_files(self.mock_passenger_data, self.mock_routes_data, "data/_passengers.json", "data/_routes.json")
        self.routeCost._update_routes()

    @classmethod
    def tearDownClass(cls):
        os.remove("data/_passengers.json")
        os.remove("data/_routes.json")

    def test_1_passenger_names(self):
        expected = ["ім'я1 прізвище1 по-батькові1", "ім'я2 прізвище2 по-батькові2", "ім'я3 прізвище3 по-батькові3"]
        res = self.routeCost._get_passenger_names()
        self.assertIsInstance(res, list)
        self.assertCountEqual(expected, res)
        self.assertListEqual(expected, res)

    def test_2_load_passenger(self):
        expected_from = "місто2"
        expected_to = "місто10"
        res = self.routeCost._load_passenger("ім'я2 прізвище2 по-батькові2")
        self.assertEqual(expected_from, res._from_city)
        self.assertEqual(expected_to, res._to_city)

    def test_3_change_route(self):
        self.routeCost._change_passenger_route("ім'я1 прізвище1 по-батькові1", "місто2", "місто10")
        expected_from = "місто2"
        expected_to = "місто10"
        res = self.routeCost._load_passenger("ім'я1 прізвище1 по-батькові1")
        self.assertEqual(expected_from, res._from_city)
        self.assertEqual(expected_to, res._to_city)

    def test_4_add_passenger(self):
        self.routeCost._add_passenger("test_name", "test_from", "test_to")
        expected = ["ім'я1 прізвище1 по-батькові1", "ім'я2 прізвище2 по-батькові2", "ім'я3 прізвище3 по-батькові3", "test_name"]
        res = self.routeCost._get_passenger_names()
        self.assertIsInstance(res, list)
        self.assertCountEqual(expected, res)
        self.assertListEqual(expected, res)

    def test_5_add_route(self):
        self.routeCost._add_route("test_city_1", "test_city_2", 1000)
        res = self.routeCost._routes
        self.assertTrue(len(res) == 4)
        for el in res:
            self.assertTrue(len(el) == 3)
            self.assertIsInstance(el[2], float)
            if el[0] == "test_city_1" and el[1] == "test_city_2":
                self.assertAlmostEqual(1000, el[2])

if __name__ == "__main__":
    unittest.main(verbosity = 2)
    
