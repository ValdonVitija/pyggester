from _ast import AST, Assert, Assign, ClassDef, Expr, Module, Tuple
import ast
import inspect
from astor import to_source
from typing import Any, ClassVar, Tuple, Union, Set
import pathlib
from helpers import source_code_to_str


class ObservableListWrapper(ast.NodeTransformer):
    """AST transformer to wrap lists with ObservableList."""

    __slots__: Tuple[str] = ()

    def visit_List(self, node: ast.List) -> Union[ast.Call, ast.AST]:
        """
        Transform a List node to an ObservableList node.

        Args:
            node (ast.List): The original List node.

        Returns:
            Union[ast.Call, ast.AST]: The transformed node.
        """
        return ast.Call(
            func=ast.Name(id="ObservableList", ctx=ast.Load()), args=[node], keywords=[]
        )


class ObservableDictWrapper(ast.NodeTransformer):
    """AST transformer to wrap dicts with ObservableDict."""

    __slots__: Tuple[str] = ()

    def visit_Dict(self, node: ast.Dict) -> Union[ast.Call, ast.AST]:
        """
        Transform a Dict node to an ObservableDict node.

        Args:
            node (ast.Dict): The original Dict node.

        Returns:
            Union[ast.Call, ast.AST]: The transformed node.
        """
        return ast.Call(
            func=ast.Name(id="ObservableDict", ctx=ast.Load()), args=[node], keywords=[]
        )


class ObservableTupleWrapper(ast.NodeTransformer):
    """AST transformer to wrap tuples with ObservableTuple."""

    __slots__: Tuple[str] = ()

    def visit_Tuple(self, node: ast.Tuple) -> Union[ast.Call, ast.AST]:
        """
        Transform a Tuple node to an ObservableTuple node.

        Args:
            node (ast.Tuple): The original Tuple node.

        Returns:
            Union[ast.Call, ast.AST]: The transformed node.
        """
        return ast.Call(
            func=ast.Name(id="ObservableTuple", ctx=ast.Load()),
            args=[node],
            keywords=[],
        )


class ObservableSetWrapper(ast.NodeTransformer):
    """AST transformer to wrap tuples with ObservableTuple."""

    __slots__: Tuple[str] = ()

    def visit_Set(self, node: ast.Set) -> Union[ast.Call, ast.AST]:
        """
        Transform a Set node to an ObservableSet node.

        Args:
            node (ast.Set): The original Tuple node.

        Returns:
            Union[ast.Call, ast.AST]: The transformed node.
        """
        return ast.Call(
            func=ast.Name(id="ObservableSet", ctx=ast.Load()),
            args=[node],
            keywords=[],
        )


class ObservableNamedTupleWrapper(ast.NodeTransformer):
    """AST transformer to wrap namedtuples with ObservableNamedTuple."""

    def __init__(self) -> None:
        self.namedtuple_instances = set()

    def visit_Module(self, node: Module) -> Any:
        print(ast.dump(node, indent=4))

    def visit_Assign(self, node: Assign) -> Any:
        # print(ast.dump(node, indent=4))
        # for target in node.targets:
        if getattr(node, "value") and isinstance(node.value, ast.Call):
            if getattr(node.value, "func"):
                if isinstance(node.value.func, ast.Name):
                    if node.value.func.id == "namedtuple":
                        for target in node.targets:
                            if isinstance(target, ast.Name):
                                print("here")
                                self.namedtuple_instances.add(target.id)

        print(self.namedtuple_instances)
        # if isinstance(target, ast.Name):
        # target.id
    def visit_Expr(self, node: Expr) -> Any:

    # def visit_Call(self, node: ast.Call) -> Union[ast.Call, ast.AST]:
    #     """
    #     Transform a Call node to an ObservableNamedTuple node.

    #     Args:
    #         node (ast.Call): The original Call node.

    #     Returns:
    #         Union[ast.Call, ast.AST]: The transformed node.
    #     """
    #     if (
    #         isinstance(node.func, ast.Name)
    #         and node.func.id == self.typename
    #         and isinstance(node.args[0], ast.Tuple)
    #     ):
    #         return ast.Call(
    #             func=ast.Name(id="ObservableNamedTuple", ctx=ast.Load()),
    #             args=[node],
    #             keywords=[],
    #         )
    #     return node


class WrapperCollector(ast.NodeVisitor):
    """
    AST visitor to collect class names that are wrappers.
    """

    __slots__: Tuple[str] = ("observables",)

    def __init__(self) -> None:
        """
        Initialize the WrapperCollector.

        The observables set is used to store the names of wrapper classes.
        """
        self.observables: Set[str] = set()

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        """
        Visit a ClassDef node.

        If the class name is not the same as the WrapperCollector class name,
        add the class name to the observables set, because this class is only used to automatically
        collector ObservableWrappers.

        Args:
            node (ast.ClassDef): The ClassDef node to visit.
        """
        if node.name != self.__class__.__name__:
            self.observables.add(node.name)


def get_wrappers_as_strings() -> Set[str]:
    """
    Get observable wrappers as a set of strings.
    This will be used by module importer to import these wrappers in each module selected for
    transformation

    """
    wrapper_visitor = WrapperCollector()
    wrapper_visitor.visit(ast.parse(source_code_to_str(path=pathlib.Path(__file__))))
    return wrapper_visitor.observables


def add_observable_wrappers(source_code):
    tree = ast.parse(source_code)

    # list_transformer = ObservableListWrapper()
    # dict_transformer = ObservableDictWrapper()
    namedtuple_transformer = ObservableNamedTupleWrapper()

    # for transformer in (list_transformer, dict_transformer):
    #     tree = transformer.visit(tree)
    tree = namedtuple_transformer.visit(tree)
    # return to_source(tree)
    return ast.unparse(tree)


# Example usage
original_code = """
my_list = [1, 2, 3]
my_dict = {'a': 1, 'b': 2}
Person = namedtuple('Person'['name', 'age'])
Person(name="sdsd", age=22)
def func1():
    mapper: {a:1, b:2}
"""

wrapped_code = add_observable_wrappers(original_code)

# Output the transformed code
print(wrapped_code)
