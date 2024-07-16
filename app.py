import json
import csv
import io
from itertools import combinations

def get_columns(data):
    """
    Извлекает список имен столбцов из набора данных.
    Аргументы:
        data (list of dict): Набор данных, где каждая строка представлена в виде словаря.

    Возвращает:
        list: Список имен столбцов.
    """
    columns = set()
    for row in data:
        columns.update(row.keys())
    return list(columns)

def is_duplicates(data, columns):
    """
    Проверяет, есть ли в наборе данных дубликаты строк на основе указанных столбцов.

    Аргументы:
        data (list of dict): Набор данных, где каждая строка представлена в виде словаря.
        columns (list of str): Список столбцов для проверки на дубликаты.

    Возвращает:
        bool: True, если найдены дубликаты, иначе False.
    """
    seen = set()
    i = 0
    while i < len(data):
        row = data[i]
        row_tuple = tuple((col, row.get(col, None)) for col in columns)
        if row_tuple in seen:
            return True
        seen.add(row_tuple)
        i += 1
    return False

def column_unique_counts(data, columns):
    """
    Вычисляет количество уникальных значений для каждого столбца в наборе данных.

    Аргументы:
        data (list of dict): Набор данных, где каждая строка представлена в виде словаря.
        columns (list of str): Список столбцов для подсчета уникальных значений.

    Возвращает:
        dict: Словарь, где ключи - имена столбцов, а значения - количество уникальных значений.
    """
    unique_counts = {}
    i = 0
    while i < len(columns):
        column = columns[i]
        unique_values = set()
        j = 0
        while j < len(data):
            row = data[j]
            unique_values.add(row.get(column, None))
            j += 1
        unique_counts[column] = len(unique_values)
        i += 1
    return unique_counts

def main(str_data):
    """
    Определяет минимальный набор столбцов, необходимых для уникальной идентификации каждой строки в наборе данных.

    Аргументы:
        str_data (str): Строковое представление набора данных в формате JSON.

    Возвращает:
        list: Минимальный список столбцов, которые уникально идентифицируют каждую строку.
    """
    # Парсинг JSON-строки в список словарей
    data = json.loads(str_data)

    # Получение списка имен столбцов
    columns = get_columns(data)

    # Определение необходимых столбцов, которые точно будут присутствовать в результате:
    # по очереди, исключаем один из столбцов и смотрим есть ли дубликаты. Если есть, то исключённый столбец обязательный
    necessary_cols = []
    i = 0
    while i < len(columns):
        column = columns[i]
        if is_duplicates(data, [col for col in columns if col != column]):
            necessary_cols.append(column)
        i += 1

    # Все остальные стобцы - вероятные.
    probable_cols = []
    i = 0
    while i < len(columns):
        column = columns[i]
        if column not in necessary_cols:
            probable_cols.append(column)
        i += 1

    # Подсчёт количества уникальных значений для вероятных столбцов:
    probable_unique_counts = column_unique_counts(data, probable_cols)
    # Сортировка вероятных столбцов по количеству уникальных значений
    sorted_probable_cols = sorted(probable_unique_counts, key=probable_unique_counts.get, reverse=True)

    # Перебор комбинаций вероятных столбцов для нахождения минимального уникального набора.
    r = 0
    while r <= len(sorted_probable_cols):
        comb = combinations(sorted_probable_cols, r)
        subset = next(comb, None)
        while subset is not None:
            subset_columns = list(subset) + necessary_cols
            if not is_duplicates(data, subset_columns):
                result = subset_columns
                # Преобразование списка имен столбцов в CSV-строку
                output = io.StringIO()
                writer = csv.writer(output)
                for col in result:
                    writer.writerow([col])
                return output.getvalue()
            subset = next(comb, None)
        r += 1

    # если уникальный набор не найден
    return ""
