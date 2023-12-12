from typer.testing import CliRunner
from pyggester.cli import app

runner = CliRunner()


def test_static_analysis():
    result = runner.invoke(app, ["static", "--path", "test_file.py"])
    assert result.exit_code == 0


def test_dynamic_transformation():
    result = runner.invoke(app, ["transform", "tests/test_file.py"])
    assert result.exit_code == 0


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
