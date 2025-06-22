import pytest
import csv
import sys
import os
# Для тестов измените на свой путь
sys.path.append("/home/kript/PycharmProjects/testing/CSV_Browser")
from view.console.csv_io import CsvIO


@pytest.fixture
def sample_csv_file(tmp_path):
    """Создаёт временный CSV-файл для тестирования."""
    csv_data = [
        ["Name", "Age", "Height"],
        ["Alice", "25", "165.5"],
        ["Bob", "30", "180.2"],
        ["Charlie", "35", "175.0"]
    ]
    file_path = tmp_path / "test.csv"
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(csv_data)
    return file_path


@pytest.fixture
def csv_io():
    return CsvIO()


def test_initialization(csv_io):
    assert csv_io.columns == []
    assert csv_io.data == []
    assert csv_io.cleaned_data == []


def test_clean_object():
    assert CsvIO.clean_object("123") == 123
    assert CsvIO.clean_object("123.45") == 123.45
    assert CsvIO.clean_object("text") == "text"
    assert CsvIO.clean_object("") == ""


def test_read_and_clean(csv_io, sample_csv_file):
    result = csv_io.read_and_clean(str(sample_csv_file))

    # Проверка структуры данных
    assert len(csv_io.data) == 4
    assert len(csv_io.cleaned_data) == 4
    assert csv_io.columns == ["Name", "Age", "Height"]

    # Проверка типов данных в cleaned_data
    assert isinstance(csv_io.cleaned_data[1][1], int)  # Age -> int
    assert isinstance(csv_io.cleaned_data[1][2], float)  # Height -> float

    assert result == csv_io.cleaned_data

def test_print(capsys, csv_io, sample_csv_file):
    csv_io.read_and_clean(str(sample_csv_file))
    CsvIO.print(csv_io.data)

    captured = capsys.readouterr()
    assert "Alice" in captured.out
    assert "Bob" in captured.out
    assert "Charlie" in captured.out
    assert "Name" in captured.out  # Проверка заголовков


def test_repr(csv_io, sample_csv_file):
    csv_io.read_and_clean(str(sample_csv_file))
    assert repr(csv_io) == "Table rows: 4"


def test_str(csv_io, sample_csv_file):
    csv_io.read_and_clean(str(sample_csv_file))
    output = str(csv_io)
    assert "Alice" in output
    assert "Bob" in output
    assert "Charlie" in output
    assert "Name" in output


def test_empty_file(tmp_path, csv_io):
    empty_file = tmp_path / "empty.csv"
    with open(empty_file, 'w', newline='') as f:
        pass

    with pytest.raises(IndexError):
        csv_io.read_and_clean(str(empty_file))