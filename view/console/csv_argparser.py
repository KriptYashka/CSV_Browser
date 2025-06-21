import argparse



class Arguments:
    def __init__(self):
        self.args = {
            ("--file", "-f"): {"type": str, "help": "Путь к файлу", "required": True},
            ("--where", "-w"): {"type": str, "help": "Поиск по столбцам"},
            ("--aggregate", "-a"): {"type": str, "help": "Применяемая функция агрегации"},
            ("--order-by", "-o"): {"type": str, "help": "Сортировка по столбцу (может быть реализована)"},
        }

    def items(self):
        return self.args.items()


class CsvCommandParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="CSV обработчик")
        self.args = Arguments()
        for arg, params in self.args.items():
            self.parser.add_argument(*arg, **params)

    def read(self) -> argparse.Namespace:
        return self.parser.parse_args()


if __name__ == '__main__':
    parser = CsvCommandParser()
    parser.read()
