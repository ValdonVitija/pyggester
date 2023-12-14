"""
    Message Handler by default should stream messages into the standard console, but it would be 
    better if we add the capability of streaming the messages/suggestions into files with different formats
"""
from typing import List, Tuple
from pyggester.text_formatters import custom_print


class MessageHandler:
    __slots__: Tuple[str] = ("messages", "line_nr", "file_path")

    def __init__(self, line_nr, file_path) -> None:
        self.messages: List[str] = []
        self.line_nr: int = line_nr
        self.file_path: str = file_path

    def print_messages(self) -> None:
        messages__ = []
        if self.messages:
            messages__.append(f"{self.line_nr} | Suggestions({self.file_path}):")
            for message in self.messages:
                messages__.append(f"    [*] {message}")
            custom_print("\n".join(messages__), border_style="green")
