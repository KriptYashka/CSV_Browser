from abc import ABC
from typing import Iterable, Type


class BaseFilter(ABC):
    def __init__(self, data: list[list], pair: Iterable):
        self.data = data
        self.column_index, self.value = pair

    def filter(self) -> Type[NotImplementedError]:
        return NotImplementedError


class LessFilter(BaseFilter):
    def filter(self) -> list[list]:
        return [row for row in self.data if row[self.column_index] < self.value]


class LessEqualFilter(BaseFilter):
    def filter(self) -> list[list]:
        return [row for row in self.data if row[self.column_index] <= self.value]


class EqualFilter(BaseFilter):
    def filter(self) -> list[list]:
        return [row for row in self.data if row[self.column_index] == self.value]


class NotEqualFilter(BaseFilter):
    def filter(self) -> list[list]:
        return [row for row in self.data if row[self.column_index] != self.value]


class MoreFilter(BaseFilter):
    def filter(self) -> list[list]:
        return [row for row in self.data if row[self.column_index] > self.value]


class MoreEqualFilter(BaseFilter):
    def filter(self) -> list[list]:
        return [row for row in self.data if row[self.column_index] >= self.value]


class FilterController:
    def __init__(self):
        self.comparator = {
            "<=": LessEqualFilter,
            ">=": MoreEqualFilter,
            "<": LessFilter,
            ">": MoreFilter,
            "==": EqualFilter,
            "!=": NotEqualFilter
        }

    def split(self, arg_str: str):
        for comparator_symbol in self.comparator:
            if arg_str.find(comparator_symbol) != -1:
                words = arg_str.split(comparator_symbol)
                if len(words) != 2:
                    raise AttributeError("Значение параметра поиска по значению неверное")
                name, value = words
                if value.isdecimal():
                    value = float(words[1])
                return name, value, comparator_symbol

    def filter(self, data: list[list], arg_str: str):
        try:
            column_name, value, comparator_symbol = self.split(arg_str)
            column_index = data[0].index(column_name)
        except AttributeError:
            return data
        except ValueError:
            return data
        return self.comparator[comparator_symbol](data, column_index, value)


