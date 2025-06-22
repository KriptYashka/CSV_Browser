import logging
import sys
from argparse import Namespace
from functools import wraps

from logic.aggregation import AggregationHandler
from logic.filter import FilterHandler

from view.console.csv_argparser import CsvCommandParser
from view.console.csv_io import CsvIO


class CSVController:
    def __init__(self):
        self.parser = CsvCommandParser()
        self.handler = CsvIO()

        self.cmd_args = Namespace()

    @staticmethod
    def require_args(arg_name):
        """Декоратор проверки необходимого аргумента"""
        def decorator(func):
            @wraps(func)
            def wrapper(instance, *args, **kwargs):
                items = vars(instance.cmd_args)
                if arg_name in items and items[arg_name] is not None:
                    return func(instance, *args, **kwargs)
                return None
            return wrapper
        return decorator

    @require_args("where")
    def execute_filter(self, data):
        new_data, error = FilterHandler().execute(data, self.cmd_args.where)
        if error:
            logging.error("Операция фильтра не была применена: " + str(error))
        return new_data

    @require_args("aggregate")
    def execute_aggregation(self, data):
        new_data, error = AggregationHandler().execute(data, self.cmd_args.aggregate)
        if error:
            logging.error("Операция агрегации не была применена: " + str(error))
        return new_data

    def run(self):
        self.cmd_args = self.parser.read()
        data = self.handler.read_and_clean(self.cmd_args.file)
        if not data:
            return

        if filtered_data := self.execute_filter(data):
            data = filtered_data
        if aggregated_data := self.execute_aggregation(data):
            data = aggregated_data

        self.handler.print(data)
