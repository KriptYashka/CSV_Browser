import csv
import logging
import os.path
from typing import List, Optional, Any

import tabulate


class CsvIO:
    def __init__(self, path: Optional[str] = None):
        self.columns = []
        self.data = []
        self.cleaned_data = []

    def clear(self):
        self.data.clear()
        self.columns.clear()
        self.cleaned_data.clear()

    @staticmethod
    def clean_object(x):
        types_in_order = [int, float]
        for type_selected in types_in_order:
            try:
                return type_selected(x)
            except Exception as e:
                pass
        return x

    def clean_data(self):
        for row_i in range(len(self.data)):
            new_row = list(map(self.clean_object, self.data[row_i]))
            self.cleaned_data.append(new_row)

    def read_and_clean(self, path: str) -> Optional[list[list[Any]]]:
        if not os.path.exists(path):
            logging.error(f"Файла по указанному пути {path} не существует")
            return None

        self.clear()
        logging.info(f"Записаны новые данные")
        with open(path) as file:
            reader = csv.reader(file)
            for row in reader:
                self.data.append(row)

            self.columns = self.data[0]
            self.clean_data()
            return self.cleaned_data

    @staticmethod
    def print(data):
        print(tabulate.tabulate(data, headers="firstrow", tablefmt="grid"))

    def __repr__(self):
        return f"Table rows: {len(self.data)}"

    def __str__(self):
        return tabulate.tabulate(self.data, headers="firstrow", tablefmt="grid")



if __name__ == '__main__':
    reader2 = CsvIO("../../test.csv")
    reader2.read_and_clean()
    print(*reader2.data, sep="\n")
