import unittest
from main import get_weather_by_city, generate_random_joke, translate_message


class TestMinet(unittest.TestCase):
    def test_weather(self):
        data = get_weather_by_city("Москва")

        self.assertIsNotNone(data)
        self.assertEqual(data["sys"]["country"], "RU")
        self.assertEqual(data["name"], "Moscow")

    def test_joke(self):
        joke = generate_random_joke()

        self.assertTrue(isinstance(joke, str))
        self.assertGreaterEqual(len(joke), 3)

    def test_translate(self):
        text = translate_message("Russia")
        self.assertEqual(text, "Россия")

        text = translate_message("Moscow")
        self.assertEqual(text, "Москва")

        text = translate_message("Book")
        self.assertEqual(text, "Книга")
