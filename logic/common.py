def split(comparator, arg_str: str):
    for comparator_symbol in comparator:
        if arg_str.find(comparator_symbol) != -1:
            words = arg_str.split(comparator_symbol)
            if len(words) != 2:
                raise AttributeError("В условии несколько знаков сравнения")
            name, value = words
            if value.isdecimal():
                value = float(words[1])
            return name, value, comparator_symbol
    raise AttributeError("В условии отсутствует знак сравнения")


def clean_object(x):
    types_in_order = [int, float]
    for type_selected in types_in_order:
        try:
            return type_selected(x)
        except Exception as e:
            pass
    return x


def parse_arg_str(arg_str, columns, split_symbols="="):
    column_name, value, comparator_symbol = split(split_symbols, arg_str)
    if column_name not in columns:
        raise AttributeError(f"Колонки {column_name} нет в таблице")
    column_index = columns.index(column_name)
    value = clean_object(value)
    return column_index, comparator_symbol, value
