from typer.testing import CliRunner
from pyggester.cli import app

runner = CliRunner()


def test_static_analysis():
    result = runner.invoke(app, ["static", "--path", "test_file.py"])
    assert result.exit_code == 0
    assert "Running static analysis" in result.output


def test_dynamic_transformation():
    result = runner.invoke(app, ["transform", "test_file.py"])
    print(result)
    assert result.exit_code == 0
    assert "Running dynamic transformation" in result.output


def test_help():
    result = runner.invoke(app, ["static", "--help"])
    assert result.exit_code == 0
    assert "Get full documentation" in result.output


def test_get_app():
    app_instance = app.get_app()
    assert app_instance is not None
