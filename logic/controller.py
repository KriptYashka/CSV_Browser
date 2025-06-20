from view.console.csv_argparser import CSVCommandParser
from view.console.reader import CSVReader


class CSVController:
    def __init__(self):
        self.parser = CSVCommandParser()
        self.reader = CSVReader()
        self.viewer = ...

    def run(self):
        args = self.parser.read()
        data = self.reader.read_and_clean(args.file)

