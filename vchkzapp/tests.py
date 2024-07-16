from django.test import TestCase
from app import main
import csv
import io


class TestMainFunction(TestCase):

    def parse_csv(self, csv_str):
        """
        Вспомогательная функция для парсинга CSV-строки в список.
        """
        reader = csv.reader(io.StringIO(csv_str))
        next(reader)  # Пропустить заголовок
        return [row[0] for row in reader]

    def test_simple_key(self):
        json_str = '''
        [
            {"id": 1, "name": "Sam", "age": 20, "city": "York"},
            {"id": 2, "name": "Sam", "age": 20, "city": "York"},
            {"id": 3, "name": "Sam", "age": 20, "city": "York"}
        ]
        '''
        result = main(json_str)
        parsed_result = self.parse_csv(result)
        self.assertEqual(parsed_result, ["id"])

    def test_with_duplicates(self):
        json_str = '''
        [
            {"name": "Sam", "age": 30, "city": "York"},
            {"name": "Bob", "age": 30, "city": "York"},
            {"name": "Sam", "age": 0, "city": "York"}
        ]
        '''
        result = main(json_str)
        parsed_result = self.parse_csv(result)
        self.assertEqual(sorted(parsed_result), sorted(["name", "age"]))

    def test_with_all_duplicates(self):
        json_str = '''
        [
            {"name": "Sam", "age": 30, "city": "York"},
            {"name": "Sam", "age": 30, "city": "New York"},
            {"name": "Sam", "age": 31, "city": "York"},
            {"name": "Bob", "age": 30, "city": "York"}
        ]
        '''
        result = main(json_str)
        parsed_result = self.parse_csv(result)
        self.assertEqual(sorted(parsed_result), sorted(["name", "age", "city"]))

    # def test_one_row(self):
    #     json_str = '''
    #     [
    #         {"name": "Sam", "age": 30, "city": "York"}
    #     ]
    #     '''
    #     result = main(json_str)
    #     parsed_result = self.parse_csv(result)
    #     self.assertIn(parsed_result, ["name", "age", "city"])

    def test_minimal_columns(self):
        json_str = '''
        [
            {"name": "Alice", "age": 30, "city": "New York", "profession": "Engineer"},
            {"name": "Alice", "age": 30, "city": "Los Angeles", "profession": "Doctor"},
            {"name": "Alice", "age": 30, "city": "Chicago", "profession": "Artist"},
            {"name": "Alice", "age": 30, "city": "New York", "profession": "Doctor"}
        ]
        '''
        result = main(json_str)
        parsed_result = self.parse_csv(result)
        self.assertEqual(sorted(parsed_result), sorted(["profession", "city"]))

    def test_missing_value(self):
        json_str = '''
        [
            {"name": "Alice", "age": 30, "city": "New York", "profession": "Engineer"},
            {"name": "Alice", "city": "Los Angeles", "profession": "Doctor"},
            {"name": "Alice", "age": 30, "city": "Chicago", "profession": "Artist"},
            {"name": "Alice", "age": 30, "city": "New York", "profession": "Doctor"}
        ]
        '''
        result = main(json_str)
        parsed_result = self.parse_csv(result)
        self.assertEqual(sorted(parsed_result), sorted(["profession", "city"]))

    def test_missing_using_value(self):
        json_str = '''
        [
            {"name": "Alice", "age": 30, "city": "New York", "profession": "Engineer"},
            {"name": "Alice", "city": "New York", "profession": "Doctor"},
            {"name": "Alice", "age": 32, "city": "New York", "profession": "Artist"},
            {"name": "Alice", "age": 33, "city": "New York", "profession": "Doctor"}
        ]
        '''
        result = main(json_str)
        parsed_result = self.parse_csv(result)
        self.assertEqual(sorted(parsed_result), sorted(["age"]))
