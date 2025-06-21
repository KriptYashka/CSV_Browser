from abc import ABC
from typing import Iterable, Type, Any


class BaseFilter(ABC):
    def __init__(self, data: list[list], column_index: int, value: Any):
        self.data = data
        self.column_index, self.value = column_index, value

    def execute(self) -> Type[NotImplementedError]:
        return NotImplementedError


class LessFilter(BaseFilter):
    def execute(self) -> list[list]:
        return [row for row in self.data if row[self.column_index] < self.value]


class LessEqualFilter(BaseFilter):
    def execute(self) -> list[list]:
        return [row for row in self.data if row[self.column_index] <= self.value]


class EqualFilter(BaseFilter):
    def execute(self) -> list[list]:
        return [row for row in self.data if row[self.column_index] == self.value]


class NotEqualFilter(BaseFilter):
    def execute(self) -> list[list]:
        return [row for row in self.data if row[self.column_index] != self.value]


class MoreFilter(BaseFilter):
    def execute(self) -> list[list]:
        return [row for row in self.data if row[self.column_index] > self.value]


class MoreEqualFilter(BaseFilter):
    def execute(self) -> list[list]:
        return [row for row in self.data if row[self.column_index] >= self.value]


class FilterHandler:
    comparator = {
        "<=": LessEqualFilter,
        ">=": MoreEqualFilter,
        "<": LessFilter,
        ">": MoreFilter,
        "=": EqualFilter,
        "!=": NotEqualFilter
    }

    def split(self, arg_str: str):
        for comparator_symbol in self.comparator:
            if arg_str.find(comparator_symbol) != -1:
                words = arg_str.split(comparator_symbol)
                if len(words) != 2:
                    raise AttributeError("В условии несколько знаков сравнения")
                name, value = words
                if value.isdecimal():
                    value = float(words[1])
                return name, value, comparator_symbol
        raise AttributeError("В условии отсутствует знак сравнения")

    def execute(self, data: list[list], arg_str: str):
        try:
            columns = data[0]
            column_name, value, comparator_symbol = self.split(arg_str)
            if column_name not in columns:
                raise AttributeError(f"Колонки {column_name} нет в таблице")
            column_index = columns.index(column_name)
            filter_obj = self.comparator[comparator_symbol](data[1:], column_index, value)
            result = filter_obj.execute()
        except Exception as e:
            return data, e

        result.insert(0, columns)
        return result, None



