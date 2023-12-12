import pathlib
import tempfile
import pytest
from pyggester.helpers import (
    # fetch_files,
    source_code_to_str,
    PathMissingSourceCodeConversionError,
    not_implemented,
)


@pytest.fixture
def get_single_file_abs_path():
    return "/root/pyggester/tests/test_file.py"


@pytest.fixture
def get_code_as_str():
    code = """def func1():
    pass
"""
    return code


@pytest.fixture
def get_code_from_file(get_single_file_abs_path):
    with open(get_single_file_abs_path, "r", encoding="UTF-8") as f_stream:
        return f_stream.read()


def test_source_code_to_str_with_path(get_code_as_str, get_code_from_file):
    assert get_code_from_file == get_code_as_str


def test_source_code_to_str_without_path():
    with pytest.raises(PathMissingSourceCodeConversionError):
        source_code_to_str()


@not_implemented
def example_function():
    pass


def test_not_implemented_decorator():
    with pytest.raises(
        NotImplementedError, match="example_function is not yet implemented"
    ):
        example_function()
