import pytest
import typer
import unittest
from unittest.mock import patch, Mock
from pyggester.command_handlers import PyggestTransform
from pyggester.pyggester import PyggesterDynamic
from io import StringIO
from collections import namedtuple


@pytest.fixture
def pyggest_transform_instance():
    return PyggestTransform(path_="test_path", help_="test_help")


def test_pyggest_transform_initialization(pyggest_transform_instance):
    assert pyggest_transform_instance.path_ == "test_path"
    assert pyggest_transform_instance.help_ == "test_help"


class TestPyggestTransform(unittest.TestCase):
    @patch("pyggester.pyggester.PyggesterDynamic.run")
    def test_process_with_help(self, mock_run):
        pyggest_transform = PyggestTransform(path_="your_path", help_=True)
        with self.assertRaises(typer.Exit) as context:
            pyggest_transform.process()

        assert context.exception.__class__ == typer.Exit

    @patch("pyggester.pyggester.PyggesterDynamic.run")
    def test_process_without_help(self, mock_run):
        pyggest_transform = PyggestTransform(path_="your_path", help_=False)
        pyggest_transform.process()
        mock_run.assert_called_once()

    @patch(
        "pyggester.pyggester.PyggesterDynamic.run",
        side_effect=typer.Exit("Test Exception"),
    )
    def test_process_exception_handling(self, mock_run):
        pyggest_transform = PyggestTransform(path_="your_path", help_=True)
        with self.assertRaises(typer.Exit) as context:
            pyggest_transform.process()

        self.assertEqual(str(context.exception), "")
