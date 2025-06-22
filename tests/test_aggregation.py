import pytest
from statistics import mean
import sys
# Для тестов измените на свой путь
sys.path.append("/home/kript/PycharmProjects/testing/CSV_Browser")
from logic.aggregation import AggregationHandler


@pytest.fixture
def sample_data():
    return [
        ["Name", "Age", "Score"],
        ["Alice", 25, 85.5],
        ["Bob", 30, 90.0],
        ["Charlie", 35, 75.5],
        ["David", 25, 82.0]
    ]


@pytest.fixture
def aggregation_handler():
    return AggregationHandler()


class TestAggregationHandler:
    @pytest.mark.parametrize("arg_str,expected_value", [
        ("Age=min", 25),
        ("Age=max", 35),
        ("Age=avg", (25 + 30 + 35 + 25) / 4),
        ("Age=sum", 25 + 30 + 35 + 25),
        ("Age=count", 4),
        ("Score=min", 75.5),
        ("Score=max", 90.0),
        ("Score=avg", mean([85.5, 90.0, 75.5, 82.0])),
        ("Score=sum", 85.5 + 90.0 + 75.5 + 82.0),
        ("Score=count", 4),
    ])
    def test_valid_aggregations(self, sample_data, aggregation_handler, arg_str, expected_value):
        result, error = aggregation_handler.execute(sample_data, arg_str)
        assert error is None
        assert result == [
            [arg_str.split('=')[1]],
            [expected_value]
        ]

    @pytest.mark.parametrize("arg_str,expected_error", [
        ("InvalidColumn=min", "Column 'InvalidColumn' not found"),
        ("Age=unknown_func", "Функции агрегации unknown_func нет"),
        ("Age", "Invalid aggregation format"),
        ("=min", "Invalid aggregation format"),
        ("Age=", "Invalid aggregation format"),
    ])
    def test_invalid_aggregations(self, sample_data, aggregation_handler, arg_str, expected_error):
        result, error = aggregation_handler.execute(sample_data, arg_str)
        assert error is not None
        assert expected_error in str(error)

    def test_empty_data(self, aggregation_handler):
        empty_data = [["Name", "Age"]]
        result, error = aggregation_handler.execute(empty_data, "Age=min")
        assert error is None
        assert result == [
            ["min"],
            [None]
        ]

    def test_argmin_argmax(self, sample_data, aggregation_handler):
        result, error = aggregation_handler.execute(sample_data, "Score=argmin")
        assert error is None
        assert result == [
            ["argmin"],
            [2]
        ]

        result, error = aggregation_handler.execute(sample_data, "Score=argmax")
        assert error is None
        assert result == [
            ["argmax"],
            [1]
        ]