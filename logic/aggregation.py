from statistics import mean

from logic.common import parse_arg_str


class AggregationHandler:
    functions = {
        "min": min,
        "max": max,
        "argmin": lambda x: x.index(min(x)),
        "argmax": lambda x: x.index(max(x)),
        "avg": mean,
        "sum": sum,
        "count": len,

    }

    def execute(self, data: list[list], arg_str: str):
        try:
            columns = data[0]
            column_index, comparator_symbol, func_name = parse_arg_str(arg_str, columns)
            if func_name not in self.functions:
                raise AttributeError(f"Функции агрегации {func_name} нет")

            col_values = [data[row_index][column_index] for row_index in range(1, len(data))]

            value = self.functions[func_name](col_values)
            result = [
                [func_name],
                [value]
            ]
            return result, None

        except Exception as e:
            return data, e

