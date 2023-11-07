from _ast import Assign, ClassDef, Module
import ast
from typing import Any, List, Dict, ClassVar, Union

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
    "ListAnalyzer",
    "DictAnalyzer",
    "SetAnalyzer",
    "TupleAnalyzer",
]


class ListAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.lists__: Dict[str, Dict[str, Union[str, int, bool]]] = {}
        self.messages__: Dict[str, Union[str, int]] = {}

    # def visit(self, node):
    # self.generic_visit(node)

    def visit_Module(self, node: Module) -> Any:
        print(ast.dump(node, indent=4))
        self.visit_scope(node)
        # self.generic_visit(node)

    def visit_ClassDef(self, node: ClassDef) -> Any:
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.visit_scope(node)
        self.generic_visit(node)

    def visit_For(self, node):
        self.visit_scope(node)
        self.generic_visit(node)

    def visit_While(self, node):
        self.visit_scope(node)
        self.generic_visit(node)

    def visit_Assign(self, node: Assign) -> Any:
        # self.visit_scope(node)
        self.get_list_declarations(node)

    def visit_scope(
        self,
        node,
    ):
        # print(node)
        if isinstance(node, ast.Module):
            pass
        for child in ast.iter_child_nodes(node):
            print(child)
            self.get_list_declarations(child, root_node=node)
        for child in ast.iter_child_nodes(node):
            self.check_if_list_modified(child)

    # def get_list_declarations(self, node, root_node):
    #     if isinstance(node, ast.Assign):
    #         for target in node.targets:
    #             if isinstance(target, ast.Name) and isinstance(node.value, ast.List):
    #                 list_name = f"{root_node.name}%{target.id}"
    #                 self.lists__[list_name]: Dict[str, bool | int | str] = {
    #                     "modified": False,
    #                     "homogeneous": False,
    #                     "line_nr": target.lineno,
    #                 }

    def get_list_declarations(self, node, root_node):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and isinstance(node.value, ast.List):
                    list_name = f"{root_node.name}%{target.id}"
                    self.lists__[list_name]: Dict[str, bool | int | str] = {
                        "modified": False,
                        "homogeneous": False,
                        "line_nr": target.lineno,
                    }

    def check_if_list_modified(self, node) -> None:
        if isinstance(node, ast.Expr):
            for list_ in self.lists__.keys():
                if node.value.func.value.id in list_:
                    if node.value.func.attr == "append":
                        self.lists__[list_]["modified"] = True

        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Subscript):
                    for list_ in self.lists__.keys():
                        if target.value.id in list_:
                            self.lists__[list_]["modified"] = True

    def print_messages(self):
        for key, value in self.lists__.items():
            print(f"List: {key}")
            if not value["modified"]:
                print(f"List: {key.split('%')[-1]} not modified, use a tuple instead!")


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

visitor = ListAnalyzer()

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
