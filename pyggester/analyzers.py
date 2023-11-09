# from _ast import Assign, ClassDef, Expr, Module
import ast
import abc
from typing import Any, List, Dict, ClassVar, Union, Set

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


class Analyzer(abc.ABC):
    """
    This abstract class represents an analyzer. Each specific analyzer will
    have to derive from this class. It offers common analyzer traits.
    Each Analyzer attacks a specific unoptimal usage of a datastructure.

    Attributes:
        structures__: A dictionary to store information about identified lists in the code.
        messages__: A dictionary to store messages related to the analysis.
        current_module: The current module being analyzed.
        current_class: The current class being analyzed.
        current_function: The current function being analyzed.
    """

    # __slots__: ClassVar[Set[str]] = {
    #     "structures__",
    #     "message__",
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

    def __init__(self, message__, current_module, current_class, current_function):
        """
                Examples:
                    self.structures__ example:
                    {
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
        self.structures__: Dict[str, Dict[str, Union[str, int, bool]]] = {}
        self.message__: str = message__
        self.current_module: str = current_module
        self.current_class: str = current_class
        self.current_function: str = current_function


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
            message__="USE A TUPLE INSTEAD OF A LIST",
            current_module="",
            current_class="",
            current_function="",
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
        self.current_class: str = node.name
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
        self.current_function: str = node.name
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
                list_name = f"{self.current_module}%{self.current_class}%{self.current_function}%{target.id}"
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


class NumpyInsteadOfListForMatrices(ast.NodeVisitor):
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
            current_module="",
            current_class="",
            current_function="",
        )


class DictAnalyzer(ast.NodeVisitor):
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
        super().__init__(
            message__="",
            current_module="",
            current_class="",
            current_function="",
        )


class SetAnalyzer(ast.NodeVisitor):
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
        super().__init__(
            message__="",
            current_module="",
            current_class="",
            current_function="",
        )


class TupleAnalyzer(ast.NodeVisitor):
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
        super().__init__(
            message__="",
            current_module="",
            current_class="",
            current_function="",
        )


tree = ast.parse(code)

visitor = TupleInsteadOfListAnalyzer()
visitor.visit(tree)
visitor.print_messages()
