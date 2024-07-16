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

    def test_unique_identification(self):
        json_str = '''
        [
            {"id": 1, "name": "Alice", "age": 30, "city": "New York"},
            {"id": 2, "name": "Bob", "age": 25, "city": "New York"},
            {"id": 3, "name": "Alice", "age": 30, "city": "San Francisco"}
        ]
        '''
        result = main(json_str)
        parsed_result = self.parse_csv(result)
        self.assertEqual(parsed_result, ["id"])

    def test_no_duplicates(self):
        json_str = '''
        [
            {"name": "Alice", "age": 30, "city": "New York"},
            {"name": "Bob", "age": 35, "city": "New York"},
            {"name": "Charlie", "age": 35, "city": "Chicago"}
        ]
        '''
        result = main(json_str)
        parsed_result = self.parse_csv(result)
        self.assertEqual(parsed_result, ["name"])

    def test_with_duplicates(self):
        json_str = '''
        [
            {"id": 1, "name": "Alice", "age": 30, "city": "New York"},
            {"id": 1, "name": "Alice", "age": 30, "city": "Los Angeles"},
            {"id": 1, "name": "Bob", "age": 30, "city": "Los Angeles"}
        ]
        '''
        result = main(json_str)
        parsed_result = self.parse_csv(result)
        self.assertEqual(sorted(parsed_result), sorted(["name", "city"]))

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
