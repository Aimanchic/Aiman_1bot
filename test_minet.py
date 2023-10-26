import unittest
from src.main import get_weather_by_city


class TestMinet(unittest.TestCase):
    def test_weather(self):
        data = get_weather_by_city("Москва")

        self.assertIsNotNone(data)
        self.assertEqual(data["sys"]["country"], "RU")
        self.assertEqual(data["name"], "Moscow")
