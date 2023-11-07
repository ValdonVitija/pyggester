import ast
from typing import List, Dict, ClassVar, Union

code = """
def modify_list():
    list_1 = [1, 2, 3]
    list_2 = [1,4,5,4,2,3]
    list_1.append("4")  # Modification
    list_1[0] = 0     # Modification
    for x in list_2:
        print(x)

"""

__all__: List[str] = [
    "ListAnalyzer",
    "DictAnalyzer",
    "SetAnalyzer",
    "TupleAnalyzer",
]


class ListAnalyzer(ast.NodeVisitor):
    """
    ListAnalyzer will be used to analyse the usage of the list datastructure through your code.
    This class supports the following suggestions:
    """

    __slots__: ClassVar[List[str]] = [
        "lists__",
        "messages__",
    ]

    def __init__(self) -> None:
        """
        self.lists__ example:
        {
        func1_list1: {
            "modified": True/False,
            "homogeneous": True/False
            "line_nr": (int)
            }
        }
        """
        self.lists__: Dict[str, Dict[str, Union[str, int, bool]]] = {}
        """
        self.messages__ example:
        {
            message: "......"
            line_nr: (int)
        }
        """
        self.messages__: Dict[str, Union[str, int]] = {}

    def visit_FunctionDef(self, node) -> None:
        """
        1. First get all list declarations in all function scopes
        2. Check if the list has been modified. If we append or we change an element at a specific position

        """
        for child in ast.iter_child_nodes(node):
            self.get_list_declarations(child, root_node=node)
        for child in ast.iter_child_nodes(node):
            self.check_if_list_modified(child)

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
