import csv
from typing import List, Optional


class CSVReader:
    def __init__(self, path: Optional[str] = None):
        self.data = []
        self.cleaned_data = []

    def read_and_clean(self, path: str) -> list[list]:
        with open(path) as file:
            reader = csv.reader(file)
            for row in reader:
                self.data.append(row)
            self.clean_data()
            return self.cleaned_data

    @staticmethod
    def clean_object(x):
        types_order = [int, float]
        for type_selected in types_order:
            try:
                return type_selected(x)
            except Exception:
                pass
        return x

    def clean_data(self):
        for row_i in range(len(self.data)):
            new_row = list(map(self.clean_object, self.data[row_i]))
            self.cleaned_data.append(new_row)


if __name__ == '__main__':
    reader = CSVReader("test.csv")
    reader.read_and_clean()
    print(*reader.data, sep="\n")
