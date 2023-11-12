# from _ast import Assign, ClassDef, Expr, Module
import abc
import ast
import pathlib
from typing import Any, ClassVar, Dict, List, Set, Type, Union, Tuple
from pydantic import BaseModel, Field
from typing_extensions import Annotated


code = """
AAAAA = []
def modify_list(a: int):
    list_1 = [1, 2, 3]
    # list_2 = [1,4,5,4,2,3]
    list_1.append("4")  # Modification
    list_1[0] = 0     # Modification
    lista_ = []
    for x in range(10):
        lista_.append(x)

class A():
    def func1_a():
        karakteret = []
"""

__all__: List[str] = [
    "TupleInsteadOfListAnalyzer",
    "DictAnalyzer",
    "SetAnalyzer",
    "TupleAnalyzer",
]


class PathConfig(BaseModel):
    """
    Represents a specific path to the data structure starting from the highest level.

    The path can take various forms:
    - For the current module, it includes the full path from the root directory (repository directory level).
    This is represented as a `pathlib.Path` object instead of a string.

    Possible variations:
    - [*] Module
    - [*] Module -> Function
    - [*] Module -> Class -> Function
    """

    # current_module: Annotated[pathlib.Path, Field(default=pathlib.Path(""))]
    current_module: Annotated[str, Field(default="")]
    current_class: Annotated[str, Field(default="")]
    current_function: Annotated[str, Field(default="")]


class Analyzer(abc.ABC):
    """
    Abstract base class for data structure analyzers. Derive specific analyzers
    from this class to address suboptimal usage patterns in data structures.

    This class defines common traits for analyzers, each designed to identify
    and rectify specific inefficiencies within data structures. Analyzers play
    a crucial role in optimizing and enhancing the performance of data-related
    operations by pinpointing and addressing unoptimal usage.

    To create a new analyzer, inherit from this class and implement the
    necessary methods to analyze and optimize the targeted data structure.

    Attributes:
        structures__: A dictionary to store information about identified lists in the code.
        messages__: A dictionary to store messages related to the analysis.
        current_module: The current module being analyzed.
        current_class: The current class being analyzed.
        current_function: The current function being analyzed.
    ---------------------------------------------------------------------------------
    Examples:
    structures__ = {
            func1_list1: {
                    "modified": True/False,
                    "line_nr": (int)
                    }
                }



        COULD BE:

        structures__ = {
            "module": {
                "classes": {
                    "class1": {
                        "functions": {
                            "func1": {
                                "lists": {
                                    "numbers_1",
                                    "numbers_2"
                                }
                            }
                        }
                    }
                }
            }
        }
    """

    # __slots__: ClassVar[Set[str]] = {
    #     "structures__",
    #     "message__",a
    #     "current_module",
    #     "current_class",
    #     "current_function",
    # }

    # # NOTE: The following is just a work around for __slots__ not being part of the class inheritance contract

    # def __setattr__(self, __name: str, __value: Any) -> None:
    #     if __name not in self.__slots__:
    #         raise AttributeError(
    #             f"'{self.__class__.__name__}' object has no attribute '{__name}'"
    #         )
    #     super().__setattr__(__name, __value)

    def __init__(self, message__, pathconfig: PathConfig):
        self.structures__: Dict[str, Dict[str, Union[str, int, bool]]] = {}
        self.message__: str = message__
        self.pathconfig: PathConfig = pathconfig


class TupleInsteadOfListAnalyzer(Analyzer, ast.NodeVisitor):
    """
    This class analyzes Python code using an ast-based approach to analyze
    when a list has been used instead of a tuple

    """

    __slots__: ClassVar[Set[str]] = {
        "structures__",
        "message__",
        "current_module",
        "current_class",
        "current_function",
    }

    def __init__(self):
        super().__init__(
            message__="USE A TUPLE INSTEAD OF A LIST", pathconfig=PathConfig()
        )

    def visit_Module(self, node: ast.Module) -> Any:
        """
        Visit a Module node in the AST.

        Args:
            node: The Module node in the AST.

        Returns:
            Any
        """
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        """
        Visit a ClassDef node in the AST.
        Since for each python module in the analysis this class will be initialized, this method
        should set the current class being analyzed by the ast module, to help us construct
        a unique name for each list
        Args:
            node: The ClassDef node in the AST.

        Returns:
            Any
        """
        self.pathconfig.current_class: str = node.name
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        """
        Visit a FunctionDef node in the AST.
        Since for each python module in the analysis this class will be initialized, this method
        should set the current function being analyzed by the ast module, to help us construct
        a unique name for each list
        Args:
            node: The FunctionDef node in the AST.

        Returns:
            Any
        """
        self.pathconfig.current_function: str = node.name
        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> Any:
        """
        Visit a For node in the AST.

        Args:
            node: The For node in the AST.

        Returns:
            Any
        """
        self.generic_visit(node)

    def visit_While(self, node: ast.While) -> Any:
        """
        Visit a While node in the AST.

        Args:
            node: The While node in the AST.

        Returns:
            Any
        """
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> Any:
        """
        Visit an Assign node in the AST.

        Args:
            node: The Assign node in the AST.

        Returns:
            Any
        """
        for target in node.targets:
            if isinstance(target, ast.Name) and isinstance(node.value, ast.List):
                list_name = f"{self.pathconfig.current_module}%{self.pathconfig.current_class}%{self.pathconfig.current_function}%{target.id}"
                self.structures__[list_name]: Dict[str, bool | int | str] = {
                    "modified": False,
                    "line_nr": target.lineno,
                }

            if isinstance(target, ast.Subscript):
                for list_, _ in self.structures__.items():
                    if target.value.id in list_:
                        self.structures__[list_]["modified"] = True

    def visit_Expr(self, node: ast.Expr) -> Any:
        """
        Visit an Expr node in the AST.

        Args:
            node: The Expr node in the AST.

        Returns:
            Any
        """
        for list_, _ in self.structures__.items():
            if node.value.func.value.id in list_:
                if node.value.func.attr == "append":
                    self.structures__[list_]["modified"] = True

    def print_messages(self):
        for _, value in self.structures__.items():
            if not value["modified"]:
                print(f"Line nr: {value['line_nr']} | {self.message__}")

    # def __iter__(self):
    #     """
    #     Since after each analyzer finishes its processing, we
    #     need to access the structures__ attribute to fetch information
    #     that has been stored during processing, we are converting
    #     these analyzer objects into iterables, so that we iterate
    #     over each structure per analzyer specifically.
    #     This way we can iterate using the same way in all the
    #     analzyers but the presented information might be different
    #     since its structure could be different.
    #     """
    #     # return iter(self.structures__.items())
    #     report__ = set()
    #     for _, value in self.structures__.items():
    #         if not value["modified"]:
    #             report__.add(f"Line nr: {value['line_nr']} | {self.message__}")

    #     return iter(report__)


class NumpyInsteadOfListForMatrices(Analyzer, ast.NodeVisitor):
    """
    NumpyInsteadOfListForMatrices will be used to analyse the usage of the list datastructure to represent
    a matrix instead of using a numpy. Numpy offers a better matrix manipulation api. Faster, simpler, more readable.
    """

    __slots__: ClassVar[Set[str]] = {
        "structures__",
        "message__",
        "current_module",
        "current_class",
        "current_function",
    }

    def __init__(self):
        super().__init__(
            message__="USE A NUMPY INSTEAD OF A LIST FOR MATRIX REPRESENATION AND MANIPULATION",
            pathconfig=PathConfig(),
        )


class DictAnalyzer(Analyzer, ast.NodeVisitor):
    """
    DictAnalyzer will be used to analyse the usage of the dict datastructure through your code.
    This class supports the following suggestions:
    """

    __slots__: ClassVar[Set[str]] = {
        "structures__",
        "message__",
        "current_module",
        "current_class",
        "current_function",
    }

    def __init__(self):
        super().__init__(message__="", pathconfig=PathConfig())


class SetAnalyzer(Analyzer, ast.NodeVisitor):
    """
    SetAnalyzer will be used to analyse the usage of the set datastructure through your code.
    This class supports the following suggestions:
    """

    __slots__: ClassVar[Set[str]] = {
        "structures__",
        "message__",
        "current_module",
        "current_class",
        "current_function",
    }

    def __init__(self):
        super().__init__(message__="", pathconfig=PathConfig())


class TupleAnalyzer(Analyzer, ast.NodeVisitor):
    """
    TupleAnalyzer will be used to analyse the usage of the tuple datastructure through your code.
    This class supports the following suggestions:
    """

    __slots__: ClassVar[Set[str]] = {
        "structures__",
        "message__",
        "current_module",
        "current_class",
        "current_function",
    }

    def __init__(self):
        super().__init__(message__="", pathconfig=PathConfig())


# def get_analyzers():
#     """
#     Instead of having to import each analyzer on its own from the pyggester module,
#     we instead construct a structure that represents all different analyzer categories
#     """
#     analyzers = {
#         "lists": {
#             TupleInsteadOfListAnalyzer,
#         },
#         "dicts": {
#             DictAnalyzer,
#         },
#         "sets": {},
#         "tuples": {},
#         "namedtuples": {},
#         "queues": {},
#         "arrays": {},
#         "deques": {},
#         "strings": {},
#     }
#     return analyzers


# class AnalyzerCategory(BaseModel):
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

#     analyzer_types: set[Type]


# class AnalyzerCategory(BaseModel):
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

#     analyzer_iterator_pair: Set[Tuple[Type, Type]]


# class AnalyzerMappingModel(BaseModel):
#     """
#     Represents each analyzer specifically
#     """

#     lists: Annotated[AnalyzerCategory, "Analyzers/Message Iterators for Lists"] = {
#         "analyzer_iterator_pair": {
#             (TupleInsteadOfListAnalyzer, TupleInsteadOfListAnalyzerMessageIterator)
#         }
#     }
# dicts: Annotated[AnalyzerCategory, "Analyzers for Dicts"] = {
#     "analyzer_iterator_pair": set(frozenset())
# }
# sets: Annotated[AnalyzerCategory, "Analyzers for Sets"] = {"analyzer_types": set()}
# tuples: Annotated[AnalyzerCategory, "Analyzers for Tuples"] = {
#     "analyzer_iterator_pair": set(frozenset())
# }
# namedtuples: Annotated[AnalyzerCategory, "Analyzers for NamedTuples"] = {
#     "analyzer_iterator_pair": set(frozenset())
# }
# queues: Annotated[AnalyzerCategory, "Analyzers for Queues"] = {
#     "analyzer_iterator_pair": set(frozenset())
# }
# arrays: Annotated[AnalyzerCategory, "Analyzers for Arrays"] = {
#     "analyzer_iterator_pair": set(frozenset())
# }
# deques: Annotated[AnalyzerCategory, "Analyzers for Deques"] = {
#     "analyzer_iterator_pair": set(frozenset())
# }
# strings: Annotated[AnalyzerCategory, "Analyzers for Strings"] = {
#     "analyzer_iterator_pair": set(frozenset())
# }


# def get_analyzers() -> AnalyzerMappingModel:
#     """
#     Instead of having to import each analyzer on its own from the pyggester module,
#     we instead construct a structure that represents all different analyzer categories
#     """
#     analyzers = AnalyzerMappingModel()
#     return analyzers


# tree = ast.parse(code)

# visitor = TupleInsteadOfListAnalyzer()
# visitor.visit(tree)
# visitor.print_messages()
