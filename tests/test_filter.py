import pytest
import sys
# Для тестов измените на свой путь
sys.path.append("/home/kript/PycharmProjects/testing/CSV_Browser")
from logic.filter import BaseFilter, LessFilter, LessEqualFilter, EqualFilter, NotEqualFilter, MoreFilter, \
    MoreEqualFilter, FilterHandler


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
def filter_handler():
    return FilterHandler()


class TestBaseFilter:
    def test_base_filter_raises_not_implemented(self, sample_data):
        filter = BaseFilter(sample_data[1:], 1, 30)
        with pytest.raises(NotImplementedError):
            filter.execute()


class TestConcreteFilters:
    @pytest.mark.parametrize("filter_class,column,value,expected", [
        (LessFilter,      1, 30,   [["Alice", 25, 85.5], ["David", 25, 82.0]]),
        (LessEqualFilter, 1, 30,   [["Alice", 25, 85.5], ["Bob", 30, 90.0], ["David", 25, 82.0]]),
        (EqualFilter,     1, 25,   [["Alice", 25, 85.5], ["David", 25, 82.0]]),
        (NotEqualFilter,  1, 25,   [["Bob", 30, 90.0], ["Charlie", 35, 75.5]]),
        (MoreFilter,      1, 30,   [["Charlie", 35, 75.5]]),
        (MoreEqualFilter, 1, 30,   [["Bob", 30, 90.0], ["Charlie", 35, 75.5]]),
        (EqualFilter,     2, 85.5, [["Alice", 25, 85.5]]),
        (MoreFilter,      2, 85.5, [["Bob", 30, 90.0], ["David", 25, 82.0]]),
    ])
    def test_filters(self, sample_data, filter_class, column, value, expected):
        filter = filter_class(sample_data[1:], column, value)
        result = filter.execute()
        assert result == expected


class TestFilterHandler:
    @pytest.mark.parametrize("arg_str,expected_count,expected_error", [
        ("Age<=30", 3, None),
        ("Score>85.5", 1, None),
        ("Name=Alice", 1, None),
        ("Age!=25", 2, None),
        ("Invalid>30", None, "Колонки Invalid нет в таблице"),
    ])
    def test_filter_handler(self, sample_data, filter_handler, arg_str, expected_count, expected_error):
        result, error = filter_handler.execute(sample_data, arg_str)

        if expected_error:
            assert error is not None
            assert expected_error in str(error)
        else:
            assert error is None
            assert len(result) == expected_count + 1
            assert result[0] == sample_data[0]

    def test_empty_data(self, filter_handler):
        empty_data = [["Name", "Age"]]
        result, error = filter_handler.execute(empty_data, "Age>20")
        assert error is None
        assert len(result) == 1
        assert result == empty_data