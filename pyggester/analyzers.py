# from _ast import Assign, ClassDef, Expr, Module
import ast
from typing import Any, List, Dict, ClassVar, Union, Tuple

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


class TupleInsteadOfListAnalyzer(ast.NodeVisitor):
    """
    This class analyzes Python code using an ast-based approach to track lists and their modifications.

    Attributes:
        lists__: A dictionary to store information about identified lists in the code.
        messages__: A dictionary to store messages related to the analysis.
        current_module: The current module being analyzed.
        current_class: The current class being analyzed.
        current_function: The current function being analyzed.
    """

    __slots__: ClassVar[Tuple[str]] = (
        "lists__",
        "message__",
        "current_module",
        "current_class",
        "current_function",
    )

    def __init__(self):
        """
                Examples:
                    self.lists__ example:
                    {
                        func1_list1: {
                            "modified": True/False,
                            "line_nr": (int)
                        }
                    }



        COULD BE:

        data = {
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
        self.lists__: Dict[str, Dict[str, Union[str, int, bool]]] = {}
        self.message__: str = "USE A TUPLE INSTEAD OF A LIST"
        self.current_module: str = ""
        self.current_class: str = ""
        self.current_function: str = ""

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
                self.lists__[list_name]: Dict[str, bool | int | str] = {
                    "modified": False,
                    "line_nr": target.lineno,
                }

            if isinstance(target, ast.Subscript):
                for list_ in self.lists__.keys():
                    if target.value.id in list_:
                        self.lists__[list_]["modified"] = True

    def visit_Expr(self, node: ast.Expr) -> Any:
        """
        Visit an Expr node in the AST.

        Args:
            node: The Expr node in the AST.

        Returns:
            Any
        """
        for list_ in self.lists__.keys():
            if node.value.func.value.id in list_:
                if node.value.func.attr == "append":
                    self.lists__[list_]["modified"] = True

    def print_messages(self):
        for key, value in self.lists__.items():
            if not value["modified"]:
                print(f"Line nr: {value['line_nr']} | {self.message__}")


# class ListAnalyzer(ast.NodeVisitor):
#     __slots__: ClassVar[Tuple[str]] = (
#         "lists__",
#         "messages__",
#         "current_module",
#         "current_class",
#         "current_function",
#     )

#     def __init__(self):
#         self.lists__: Dict[str, Dict[str, Union[str, int, bool]]] = {}
#         self.messages__: Dict[str, Union[str, int]] = {}
#         self.current_module: str = ""
#         self.current_class: str = ""
#         self.current_function: str = ""

#     def visit_Module(self, node: ast.Module) -> Any:
#         self.generic_visit(node)

#     def visit_ClassDef(self, node: ast.ClassDef) -> Any:
#         self.current_class: str = node.name
#         self.generic_visit(node)

#     def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
#         self.current_function: str = node.name
#         self.generic_visit(node)

#     def visit_For(self, node: ast.For) -> Any:
#         self.generic_visit(node)

#     def visit_While(self, node: ast.While) -> Any:
#         self.generic_visit(node)

#     def visit_Assign(self, node: ast.Assign) -> Any:
#         for target in node.targets:
#             if isinstance(target, ast.Name) and isinstance(node.value, ast.List):
#                 list_name = f"{self.current_module}%{self.current_class}%{self.current_function}%{target.id}"
#                 self.lists__[list_name]: Dict[str, bool | int | str] = {
#                     "modified": False,
#                     "homogeneous": False,
#                     "line_nr": target.lineno,
#                 }

#             if isinstance(target, ast.Subscript):
#                 for list_ in self.lists__.keys():
#                     if target.value.id in list_:
#                         self.lists__[list_]["modified"] = True

#     def visit_Expr(self, node: ast.Expr) -> Any:
#         for list_ in self.lists__.keys():
#             if node.value.func.value.id in list_:
#                 if node.value.func.attr == "append":
#                     self.lists__[list_]["modified"] = True


#     def print_messages(self):
#         for key, value in self.lists__.items():
#             # print(f"List: {key}")
#             if not value["modified"]:
#                 print(f"List: {key.split('%')[-1]} not modified, use a tuple instead!")


class DictAnalyzer(ast.NodeVisitor):
    """
    DictAnalyzer will be used to analyse the usage of the dict datastructure through your code.
    This class supports the following suggestions:
    """

    __slots__: ClassVar[List[str]] = [
        "dicts__",
        "messages__",
    ]

    def __init__(self) -> None:
        super().__init__()


class SetAnalyzer(ast.NodeVisitor):
    """
    SetAnalyzer will be used to analyse the usage of the set datastructure through your code.
    This class supports the following suggestions:
    """

    __slots__: ClassVar[List[str]] = [
        "sets__",
        "messages__",
    ]

    def __init__(self) -> None:
        super().__init__()


class TupleAnalyzer(ast.NodeVisitor):
    """
    TupleAnalyzer will be used to analyse the usage of the tuple datastructure through your code.
    This class supports the following suggestions:
    """

    __slots__: ClassVar[List[str]] = [
        "tuples__",
        "messages__",
    ]

    def __init__(self) -> None:
        super().__init__()


tree = ast.parse(code)

visitor = TupleInsteadOfListAnalyzer()

visitor.visit(tree)
visitor.print_messages()


# class ListAnalyzer(ast.NodeVisitor):
#     """
#     ListAnalyzer is used to analyze the usage of list data structures in your code.

#     This class provides suggestions for optimizing list usage.
#     """

#     __slots__: ClassVar[List[str]] = [
#         "lists__",
#         "messages__",
#     ]

#     def __init__(self) -> None:
#         """
#         Initialize the ListAnalyzer.

#         Examples:
#             self.lists__ example:
#             {
#                 func1_list1: {
#                     "modified": True/False,
#                     "homogeneous": True/False
#                     "line_nr": (int)
#                 }
#             }

#             self.messages__ example:
#             {
#                 message: "......"
#                 line_nr: (int)
#             }
#         """
#         self.lists__: Dict[str, Dict[str, Union[str, int, bool]]] = {}
#         self.messages__: Dict[str, Union[str, int]] = {}

#     def visit_FunctionDef(self, node) -> None:
#         """
#         Visit and analyze a function definition.

#         Args:
#             node (ast.FunctionDef): The function definition node.

#         1. First get all list declarations in all function scopes.
#         2. Check if the list has been modified (e.g., if elements are appended or changed).

#         """
#         for child in ast.iter_child_nodes(node):
#             self.get_list_declarations(child, root_node=node)
#         for child in ast.iter_child_nodes(node):
#             if isinstance(child, (ast.For, ast.Expr, ast.Assign, ast.While)):
#                 self.check_if_list_modified(child)

#         for child in ast.iter_child_nodes(node):
#             # print(child)
#             print(ast.dump(child, indent=4))
#             # for walker_ in ast.walk(child):
#             # print(walker_)

#             if isinstance(child, ast.For):
#                 main_loop_variable_ = child.target.id
#                 if getattr(child.iter, "func") and getattr(child.iter.func, "id"):
#                     iterating_with_ = child.iter.func.id

#                 if iterating_with_ == "range":
#                     for body_child_ in child.body:
#                         if isinstance(body_child_, ast.Expr):
#                             if getattr(body_child_.value, "func"):
#                                 for list_ in self.lists__.keys():
#                                     if (
#                                         body_child_.value.func.value.id in list_
#                                         and body_child_.value.func.attr == "append"
#                                     ):
#                                         for append_args_ in body_child_.value.args:
#                                             if isinstance(append_args_, ast.Name):
#                                                 if (
#                                                     append_args_.id
#                                                     == main_loop_variable_
#                                                 ):
#                                                     self.lists__[list_][
#                                                         "homogeneous"
#                                                     ] = True
#             if isinstance(child, ast.Expr):
#                 pass

#     def get_list_declarations(self, node, root_node):
#         """
#         Check for list declarations and record their details.

#         Args:
#             node (ast.AST): The current node being analyzed.
#             root_node (ast.FunctionDef): The root function node.

#         """
#         if isinstance(node, ast.Assign):
#             for target in node.targets:
#                 if isinstance(target, ast.Name) and isinstance(node.value, ast.List):
#                     list_name = f"{root_node.name}%{target.id}"
#                     self.lists__[list_name]: Dict[str, Union[str, int, bool]] = {
#                         "modified": False,
#                         "homogeneous": False,
#                         "line_nr": target.lineno,
#                     }

#     def check_if_list_modified(self, node) -> None:
#         """
#         Check if a list is modified (e.g., through append or subscript assignment).

#         Args:
#             node (ast.AST): The current node being analyzed.

#         """

#         if isinstance(node, ast.Expr):
#             for list_ in self.lists__.keys():
#                 if node.value.func.value.id in list_:
#                     if node.value.func.attr == "append":
#                         self.lists__[list_]["modified"] = True

#         elif isinstance(node, ast.Assign):
#             for target in node.targets:
#                 if isinstance(target, ast.Subscript):
#                     for list_ in self.lists__.keys():
#                         if target.value.id in list_:
#                             self.lists__[list_]["modified"] = True

#     def print_messages(self):
#         for key, value in self.lists__.items():
#             if not value["modified"]:
#                 print(f"List: {key.split('%')[-1]} not modified, use a tuple instead!")
#             if value["homogeneous"]:
#                 print(
#                     f"List: {key.split('%')[-1]} is homogeneous. Use the array module if possible"
#                 )
