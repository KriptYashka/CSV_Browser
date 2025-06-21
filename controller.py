import logging
import sys
from argparse import Namespace
from logic.filter import FilterHandler

from view.console.csv_argparser import CsvCommandParser
from view.console.csv_io import CsvIO


class CSVController:
    def __init__(self):
        self.parser = CsvCommandParser()
        self.handler = CsvIO()

        self.args = Namespace()

    def get_aggregate_function(self):
        functions = {
            "avg": None,
        }

    def execute_filter(self, data):
        if "where" not in self.args:
            return None

        new_data, error = FilterHandler().execute(data, self.args.where)

        if error:
            logging.error("Операция фильтра не была применена: " + str(error))
        return new_data

    def run(self):
        self.args = self.parser.read()
        cleaned_data = self.handler.read_and_clean(self.args.file)
        cleaned_data = self.execute_filter(cleaned_data)
        self.handler.print(cleaned_data)
