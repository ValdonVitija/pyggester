import pytest
from unittest.mock import patch
from pyggester.message_handler import MessageHandler


@pytest.mark.parametrize(
    "messages, expected_output",
    [
        (
            ["Message 1", "Message 2"],
            "42 | Suggestions(example.py):\n    [*] Message 1\n    [*] Message 2\n",
        ),
        ([], ""),
    ],
)
def test_print_messages(messages, expected_output, capsys):
    line_nr = 42
    file_path = "example.py"
    message_handler = MessageHandler(line_nr, file_path)
    message_handler.messages = messages

    message_handler.print_messages()
    captured = capsys.readouterr()

    assert captured.out == expected_output
