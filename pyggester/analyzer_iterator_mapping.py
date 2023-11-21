# # from message_iterators import TupleInsteadOfListAnalyzerMessageIterator, MessageIterator
# # from analyzers import TupleInsteadOfListAnalyzer, Analyzer

# from pyggester.message_iterators import (
#     TupleInsteadOfListAnalyzerMessageIterator,
#     MessageIterator,
# )
# from pyggester.analyzers import TupleInsteadOfListAnalyzer, Analyzer


# import ast
# from typing import Any, ClassVar, Dict, List, Set, Type, Union, Tuple
# from pydantic import BaseModel
# from typing_extensions import Annotated


# class AnalyzerModel(BaseModel):
#     """
#     Pydantic model representing an analyzer.

#     Attributes:
#         Analyzer (Type[Analyzer]): Type of the analyzer.
#         MessageIterator (Type[MessageIterator]): Type of the message iterator.
#     """

#     Analyzer: Type[Analyzer]
#     MessageIterator: Type[MessageIterator]


# class AnalyzerCategories(BaseModel):
#     """
#     Represents the overall category for analyzers.
#     Categories:
#         - lists
#         - dicts
#         - sets
#         - tuples
#         - namedtuples
#         - queues
#         - arrays
#         - deques
#         - strings
#     """

#     lists: Tuple[AnalyzerModel]
#     # dicts: Tuple[AnalyzerModel]
#     # sets: Tuple[AnalyzerModel]
#     # tuples: Tuple[AnalyzerModel]
#     # namedtuples: Tuple[AnalyzerModel]
#     # queues: Tuple[AnalyzerModel]
#     # arrays: Tuple[AnalyzerModel]
#     # deques: Tuple[AnalyzerModel]
#     # strings: Tuple[AnalyzerModel]


# MODEL = {
#     "lists": (
#         AnalyzerModel(
#             Analyzer=TupleInsteadOfListAnalyzer,
#             MessageIterator=TupleInsteadOfListAnalyzerMessageIterator,
#         ),
#     ),
#     # "dicts": (AnalyzerModel()),
#     # "sets": (AnalyzerModel()),
#     # "tuples": (AnalyzerModel()),
#     # "namedtuples": (AnalyzerModel()),
#     # "queues": (AnalyzerModel()),
#     # "arrays": (AnalyzerModel()),
#     # "deques": (AnalyzerModel()),
#     # "strings": (AnalyzerModel()),
# }


# def get_analyzer_categories() -> AnalyzerCategories:
#     """
#     Instead of having to import each analyzer on its own from the pyggester module,
#     we instead construct a structure that represents all different analyzer categories
#     """
#     analyzers = AnalyzerCategories(**MODEL)
#     return analyzers


# code = """
# AAAAA = []
# def modify_list(a: int):
#     list_1 = [1, 2, 3]
#     # list_2 = [1,4,5,4,2,3]
#     list_1.append("4")  # Modification
#     list_1[0] = 0     # Modification
#     lista_ = []
#     for x in range(10):
#         lista_.append(x)

# class A():
#     def func1_a():
#         karakteret = []
# """

# tree = ast.parse(code)

# # visitor = TupleInsteadOfListAnalyzer()
# # visitor.visit(tree)

# # TODO: THE FOLLOWING WILL BE MOVED TO pyggester.py
# analyzer_categories = get_analyzer_categories()
# for analyzer_model_item in analyzer_categories.lists:
#     analyzer = analyzer_model_item.Analyzer()
#     analyzer.visit(tree)
#     for message in analyzer_model_item.MessageIterator(analyzer):
#         print(message)
