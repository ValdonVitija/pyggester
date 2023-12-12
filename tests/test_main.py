import sys
import pytest
from unittest.mock import patch
from io import StringIO
from pyggester.main import main, PYGGESTER_LOGO


def test_main_with_help():
    with patch.object(sys, "argv", ["pyggest"]):
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            with pytest.raises(SystemExit) as e:
                main()

            assert e.value.code == 0
            output = mock_stdout.getvalue()
            assert PYGGESTER_LOGO in output


def test_main_without_help():
    with patch.object(sys, "argv", ["pyggest"]):
        with patch("pyggester.main.get_app") as mock_get_app:
            main()

    mock_get_app.assert_called_once()
