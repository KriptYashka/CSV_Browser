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
                if arg_name in instance.cmd_args and instance.cmd_args.__getattr__(arg_name) is not None:
                    return func(instance, *args, **kwargs)
                return None
            return wrapper
        return decorator

    @require_args("where")
    def execute_filter(self, data):
        data, error = FilterHandler().execute(data, self.cmd_args.where)
        if error:
            logging.error("Операция фильтра не была применена: " + str(error))
        return data

    @require_args("aggregate")
    def execute_aggregation(self, data):
        data, error = AggregationHandler().execute(data, self.cmd_args.aggregate)
        if error:
            logging.error("Операция агрегации не была применена: " + str(error))
        return data

    def run(self):
        self.cmd_args = self.parser.read()
        cleaned_data = self.handler.read_and_clean(self.cmd_args.file)

        filtered_data = self.execute_filter(cleaned_data)
        result = self.execute_aggregation(filtered_data)
        self.handler.print(result)
