import abc
import ast
import pathlib
from typing import Any, ClassVar, Dict, List, Set, Type, Union, Tuple
from pydantic import BaseModel, Field
from typing_extensions import Annotated

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

    # current_module: Annotated[str, Field(default="")]
    current_module: Annotated[pathlib.Path, Field(default=pathlib.Path(""))]
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

    def __init__(self, pathconfig: PathConfig):
        self.structures__: Dict[str, Dict[str, Union[str, int, bool]]] = {}
        # self.message__: str = message__
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

    def __init__(self, current_module):
        super().__init__(
            pathconfig=PathConfig(current_module=current_module),
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
        super().__init__(pathconfig=PathConfig())


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
        super().__init__(pathconfig=PathConfig())


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
        super().__init__(pathconfig=PathConfig())
