"""
    Should be a simple class that takes the messages from the analyzers and formats them based on a desired output. 
    Should support colored outputs, json outputs and other standard output formatters 
"""
from typing import Dict, List, Any, ClassVar, Set
from analyzers import Analyzer


class MessageIterator:
    """ """

    def __init__(self, analyzer: Analyzer, message: str) -> None:
        self.analyzer = analyzer
        self.message: str = message

    def __iter__(self) -> Set[str] | NotImplementedError:
        raise NotImplementedError


# class TupleInsteadOfListMessageInterpreter(MessageIterator):
#     """
#     Message interpreter for tuple instead of list analyzer
#     """

#     __slots__: ClassVar[Set[str]] = ["analyzer"]

#     def __init__(self, analyzer: Analyzer) -> None:
#         super().__init__(analyzer, "USE A TUPLE INSTEAD OF A LIST")

#     def __str__(self) -> str | NotImplementedError:
#         return "\n".join(
#             [
#                 f"Line nr: {value['line_nr']} | {self.message}"
#                 for _, value in self.analyzer.structures__.items()
#                 if not value["modified"]
#             ]
#         )


class TupleInsteadOfListAnalyzerMessageIterator(MessageIterator):
    """
    Message interpreter for tuple instead of list analyzer
    """

    __slots__: ClassVar[Set[str]] = ["analyzer"]

    def __init__(self, analyzer: Analyzer) -> None:
        super().__init__(analyzer, "USE A TUPLE INSTEAD OF A LIST")

    def __iter__(self):
        report__ = set()
        for _, value in self.analyzer.structures__.items():
            if not value["modified"]:
                report__.add(f"Line nr: {value['line_nr']} | {self.message}")

        return iter(report__)
