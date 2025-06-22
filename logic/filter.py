from abc import ABC
from typing import Type, Any

from logic.common import parse_arg_str


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
    comparators = {
        "<=": LessEqualFilter,
        ">=": MoreEqualFilter,
        "<": LessFilter,
        ">": MoreFilter,
        "!=": NotEqualFilter,
        "=": EqualFilter,
    }

    def execute(self, data: list[list], arg_str: str):
        try:
            columns = data[0]
            column_index, comparator_symbol, value = parse_arg_str(arg_str, columns, self.comparators.keys())

            filter_obj = self.comparators[comparator_symbol](data[1:], column_index, value)
            result = filter_obj.execute()
        except Exception as e:
            return data, e

        result.insert(0, columns)
        return result, None





