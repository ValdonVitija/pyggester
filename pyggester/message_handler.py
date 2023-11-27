"""
    Message Handler by default should stream messages into the standard console, but it would be 
    better if we add the capability of streaming the messages/suggestions into files with different formats
"""
from typing import List, Tuple


class MessageHandler:
    __slots__: Tuple[str] = ("messages", "line_nr", "file_path")

    def __init__(self, line_nr, file_path) -> None:
        self.messages: List[str] = []
        self.line_nr: int = line_nr
        self.file_path: str = file_path

    def print_messages(self) -> None:
        print(f"{self.line_nr} | Suggestions({self.file_path}):")
        for message in self.messages:
            print(f"    [*] {message}")
