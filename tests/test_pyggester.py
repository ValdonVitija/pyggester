import pytest
import tempfile
import pathlib
from unittest.mock import patch
from pyggester.pyggester import (
    PyggesterDynamic,
)


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield pathlib.Path(tmpdirname)


@pytest.fixture
def temp_file(temp_dir):
    temp_file = temp_dir / "test_file.py"
    temp_file.write_text("print('Hello, World!')", encoding="UTF-8")
    return temp_file


def test_initialization():
    path = "/path/to/directory"
    pyggester = PyggesterDynamic(path)
    assert pyggester.path_ == pathlib.Path(path).absolute()


def test_existence_check():
    with pytest.raises(FileNotFoundError):
        pyggester = PyggesterDynamic("/non/existent/path")
        pyggester.run()


def test_file_transformation(temp_file):
    pyggester = PyggesterDynamic(str(temp_file))
    pyggester.run()
    transformed_file = (
        temp_file.parent / f"{temp_file.stem}_transformed{temp_file.suffix}"
    )
    assert transformed_file.exists()


def test_directory_transformation(temp_dir, temp_file):
    with patch("builtins.input", return_value="test_file.py"):
        pyggester = PyggesterDynamic(str(temp_dir))
        pyggester.run()
        transformed_dir = temp_dir.parent / f"{temp_dir.name}_transformed"
        assert transformed_dir.exists() and transformed_dir.is_dir()
