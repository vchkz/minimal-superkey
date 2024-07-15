from django.test import TestCase
from vchkzapp.utils import main


class TestMainFunction(TestCase):

    def test_unique_identification(self):
        json_str = '''
        [
            {"id": 1, "name": "Alice", "age": 30, "city": "New York"},
            {"id": 2, "name": "Bob", "age": 25, "city": "New York"},
            {"id": 3, "name": "Alice", "age": 30, "city": "San Francisco"}
        ]
        '''
        result = main(json_str)
        self.assertIn("id", result)

    def test_no_duplicates(self):
        json_str = '''
        [
            {"name": "Alice", "age": 30, "city": "New York"},
            {"name": "Bob", "age": 35, "city": "New York"},
            {"name": "Charlie", "age": 35, "city": "Chicago"}
        ]
        '''
        result = main(json_str)
        self.assertIn("name", result)

    def test_with_duplicates(self):
        json_str = '''
        [
            {"id": 1, "name": "Alice", "age": 30, "city": "New York"},
            {"id": 1, "name": "Alice", "age": 30, "city": "Los Angeles"},
            {"id": 1, "name": "Bob", "age": 30, "city": "Los Angeles"}
        ]
        '''
        result = main(json_str)
        self.assertIn("name", result)
        self.assertIn("city", result)

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
        self.assertIn("profession", result)
        self.assertIn("city", result)
