from _ast import AST, Assert, Assign, ClassDef, Expr, Module, Tuple
import ast
import inspect
from astor import to_source
from typing import Any, ClassVar, Tuple, Union, Set
import pathlib
from helpers import source_code_to_str
from module_importer import add_imports

# from observable_runner import apply_observable_collector_transformations


# ----------------------------------------------------------

# The following wrappers are used for built-in standard python data structures.
# List of standard python data structures:

# list -> [] or list()
# dict -> {} or dict()
# set -> {} or set()
# tuple -> () or tuple()

# These datastructures can be directly derived to create a single wrappers that
# can wrap the original datastructure declarations without changing their core
# behaviour


# ----------------------------------------------------------


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


# ----------------------------------------------------------

# The following wrappers are part of the collections built-in python module.
# List of all container datatypes:

# ChainMap
# Counter
# OrderedDict
# UserDict
# UserList
# UserString
# defaultdict
# deque
# namedtuple

# These collections cannot be directly derived to create a single wrapper that
# can wrap the original datastructure declarations without changing its core
# behaviour

# ----------------------------------------------------------


class ObservableNamedTupleWrapper(ast.NodeTransformer):
    """AST transformer to wrap namedtuples with ObservableNamedTuple."""

    class NamedTupleVisitor(ast.NodeVisitor):
        """
        NamedTuple visitor to be used internally only by the outer-class.
        The purpose of this class is specifically to get all namedtuple instances
        in the current module being analyzed
        """

        def __init__(self) -> None:
            self.namedtuple_instances = set()

        def visit_Assign(self, node: ast.Assign) -> Any:
            """
            Visit each Assign node, because namedtuple declaration are all
            Assign nodes in the python's ast.
            """
            if getattr(node, "value") and isinstance(node.value, ast.Call):
                if getattr(node.value, "func"):
                    if isinstance(node.value.func, ast.Name):
                        if node.value.func.id == "namedtuple":
                            for target in node.targets:
                                if isinstance(target, ast.Name):
                                    self.namedtuple_instances.add(target.id)

    def __init__(self, tree) -> None:
        """
        Immediatly initialize the tuple visitor and collect all namedtuple constructor declarations.
        """
        self.namedtuple_visitor = self.NamedTupleVisitor()
        self.namedtuple_visitor.visit(tree)
        self.modified_nodes = []

    def visit_Assign(self, node: ast.Assign) -> Any:
        """
        Now visit each Assign node and check if that node is a namedtuple instance of a collected
        type by NamedTupleVisitor. If thats the case, wrap each instance into an ObservableNamedTupleWrapper,
        so that we can analyze its internal structure for potential suggestions.
        """
        if getattr(node, "value") and isinstance(node.value, ast.Call):
            if getattr(node.value, "func"):
                if isinstance(node.value.func, ast.Name):
                    if (
                        node.value.func.id
                        in self.namedtuple_visitor.namedtuple_instances
                    ):
                        for target in node.targets:
                            if isinstance(target, ast.Name):
                                wrapper_code = f"{target.id}_wrapper = ObservableNamedTuple(*{target.id})"
                                wrapper_node = ast.parse(wrapper_code).body[0]
                                return [node, wrapper_node]
        return node


class WrapperCollector(ast.NodeVisitor):
    """
    AST visitor to collect class names that are wrappers.
    """

    __slots__: Tuple[str] = ("observables",)

    def __init__(self) -> None:
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
            self.observables.add(node.name.split("Wrapper")[0])


def get_wrappers_as_strings() -> Set[str]:
    """
    Get observable wrappers as a set of strings.
    This will be used by module importer to import these wrappers in each module selected for
    transformation

    """
    wrapper_visitor = WrapperCollector()
    wrapper_visitor.visit(ast.parse(source_code_to_str(path=pathlib.Path(__file__))))
    return wrapper_visitor.observables


WRAPPERS = {
    "standard_containers": {
        "list": ObservableListWrapper,
        "dict": ObservableDictWrapper,
        "set": ObservableSetWrapper,
        "tuple": ObservableTupleWrapper,
    },
    "collector_containers": {"namedtuple": ObservableNamedTupleWrapper},
}


def apply_wrappers(tree: ast.AST) -> ast.AST:
    """
    Function that offers api wrapper functionality.
    This function takes the source code as a string and soley based on that does automatic
    code transformations.
    First of all it adds imports at the top of the module for ObservableWrappers
    """
    for _, wrapper in WRAPPERS["standard_containers"].items():
        tree = wrapper().visit(tree)
    for _, wrapper in WRAPPERS["collector_containers"].items():
        tree = wrapper(tree).visit(tree)

    return tree


original_code = """
import math 
import nothing 

my_list = [1, 2, 3]
my_dict = {'a': 1, 'b': 2}
Person = namedtuple('Person'['name', 'age'])
p1 = Person(name="sdsd", age=22)
def func1():
    mapper: {a:1, b:2}

Car = namedtuple('Car', ['brand','model'])
car_1 = Car(brand=tesla,model=x)
"""
