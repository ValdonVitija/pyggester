# Welcome to pyggester!

Thank you for your interest in contributing to pyggester. Whether you're a developer, designer, tester, or someone with great ideas, your contributions are valuable.

## Getting Started

1. **Fork the Repository:** Start by forking the [Project Repository](https://github.com/ValdonVitija/pyggester) on GitHub. This creates a copy of the project under your GitHub account.

    ```bash
    git clone https://github.com/ValdonVitija/pyggester.git
    ```

2. **Create a Branch:** Move into the project's directory and create a new branch for your contribution:

    ```bash
    cd pyggester
    git checkout -b your-branch-name
    ```

## Making Changes

Changes can encompass various aspects, provided they are reasonable. We welcome modifications to overall logic, naming conventions, hierarchy, and directory structure (with meticulous attention, especially for alterations to the project directory).

# Wrappers

Includes classes designed to encapsulate collections within observables. Every observable extends from ast.NodeTransformer, enabling the classes to effectively wrap individual data structures. Each specific wrapper is tailored to implement only the visitor method relevant to the data structure it encapsulates.

Built-in wrappers are all already done, because all we need to do is wrap the original
data structure declarations with observables.

Example (ObservableListWrapper):
```python
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
```

Specialized collections from the collections library in python are a bit different. We cannot directly 'dervie' from them, but we can pass by reference the declared data structure objects to our custom Observables.

Such Wrappers are:
 - ObservableNumpyArrayWrapper
 - ObservableNamedTupleWrapper
 - ObservablePandasDataFrameWrapper

Example (ObservableNumpyArrayWrapper):

```python
class ObservableNumpyArrayWrapper(ast.NodeTransformer):
    """AST transformer to wrap NumPy array instances with ObservableNumpyArray."""

    class NumpyImportsVisitor(ast.NodeVisitor):
        def __init__(self):
            self.alias_name = None
            self.alias_asname = None

        def visit_Import(self, node):
            """
            Check numpy imports, because we need to determine how to
            wrap the initiated array instances

            [*] import numpy
            [*] import numpy as np
            [*] import numpy as 'alias'
            """
            for name in node.names:
                if name.name == "numpy":
                    self.alias_name = name.name
                if name.name == "numpy" and getattr(name, "asname"):
                    self.alias_asname = name.asname

        def visit_ImportFrom(self, node):
            """
            Check 'from' numpy imports, because we need to determine how to wrao
            the initiated array instances

            [*] from numpy import array
            [*] from numpy import array as arr
            [*] from numpy import ones
            ...
            """
            if node.module == "numpy":
                for name in node.names:
                    if name.name in ["array", "zeros", "ones", "empty"]:
                        self.alias_name = name.name
                    if getattr(name, "asname"):
                        self.alias_asname = name.asname

    def __init__(self, tree) -> None:
        self.imports_visitor = self.NumpyImportsVisitor()
        self.imports_visitor.visit(tree)

    def visit_Assign(self, node: ast.Assign) -> ast.AST:
        """
        Now visit each Assign node and check if that node is a numpy array instance. If thats the case, wrap each instance into an ObservableNumpyArray,
        so that we can analyze its internal structure for potential suggestions.
        """
        if getattr(node, "value") and isinstance(node.value, ast.Call):
            if getattr(node.value, "func"):
                if isinstance(node.value.func, ast.Name):
                    id_ = self.get_alias_name()
                    if node.value.func.id == id_:
                        return self.wrap_numpy_array(node)

                elif isinstance(node.value.func, ast.Attribute):
                    id_ = self.get_alias_name()
                    if node.value.func.value.id == id_:
                        return self.wrap_numpy_array(node)

        return node

    def get_alias_name(self):
        return self.imports_visitor.alias_asname or self.imports_visitor.alias_name

    def wrap_numpy_array(self, node):
        wrapper_code = f"{node.targets[0].id}_numpy_wrapper = ObservableNumpyArray({node.targets[0].id})"
        wrapper_node = ast.parse(wrapper_code).body[0]
        return [node, wrapper_node]

```

>[!NOTE]
> Not every data structure from the collections library has a Wrapper and an Observable version right now. I expect potential contributors to work on them.


# 👀 Observables

The core functionality of pyggester revolves around observables, particularly enhanced versions of python data structures/collections that fully preserve the original functionality offered by these python data structures. These observables attempt to suggest alternative data structures if any issues are detected.

Standard built-in collections/data structures:
  - list
  - tuple
  - set
  - dict

> [!NOTE]
> Python's built-in collections can be customized by adding your own methods and variables. This lets you analyze the collection more effectively without changing its basic features.

Specialized collections(part of the collections library):
  - ChainMap
  - Counter
  - OrderedDict
  - UserDict
  - UserList
  - UserString
  - defaultdict
  - deque
  - namedtuple

Third-Party popular collections:
  - Numpy Arrays
  - Pandas DataFrame
  - Pandas Series


Abstract Observable Representation (e.g : list):
```Python
class ObservableList(list):
    """
    The ObservableList is an enhanced version of a list that
    preserves the full original functionality of a list, but
    adds more features to it so that we keep track of anything that
    potentially happens in order to do dynamic analysis to each declared
    list.
    """
    __slots__: Tuple[str] = (
        "appended",
        "extended",
        "inserted",
        "removed",
        "count_",
        "in_operator_used",
        "message_handler",
    )

    def __init__(self, *args, **kwargs) -> None:
      ...
    def append(self, item) -> None:
        super().append(item)
        self.appended = True

    def extend(self, iterable) -> None: ...
    def insert(self, index, item) -> None: ...
    def remove(self, item) -> None: ...
    def count(self, __value: Any) -> int: ...
    def __contains__(self, __key: object) -> bool: ...
    def get_list_dimension(self, lst): ...
    def check_numpy_array_instead_of_list(self): ...
    def check_array_instead_of_list(self): ...
    def can_list_be_converted_to_array(self): ...
    def check_list_to_set_conversion(self): ...
    def check_set_instead_of_list(self): ...
    def check_Counter_insteaf_of_list(self): ...
    def check_tuple_instead_of_list(self): ...
    def run(self):
        """
        Only run checkers so that we offer a better running interface
        for each observable.
        """
        self.check_array_instead_of_list()
        self.check_numpy_array_instead_of_list()
        self.check_set_instead_of_list()
        self.check_Counter_insteaf_of_list()
        self.message_handler.print_messages()

```

If you make sure to preserve the original functionality of built in collections, the folowing statements are exactly the same:
```Python
#List declarations
list_ = [1,2,3]
list_ = ObservableList([1,2,3])
list_ = ObservableList(list([1,2,3]))

#Dict declarations
dict_ = {"key":"value"}
dict_ = ObservableDict({"key":"value"})
dict_ = ObservableDict(dict({"key":"value"}))

#Tuple declarations
tuple_ = (1,2,3)
tuple_ = ObservableTuple([1,2,3])
tuple_ = ObservableTuple(tuple([1,2,3]))

#Set declarations
set_ = {1,2,3}
set_ = ObservableSet({1,2,3})
set_ = ObservableSet(set({1,2,3}))
```

 Currently, the supported observables are:

  - ObservableList
  - ObservableSet
  - ObservableTuple
  - ObservableDict
  - ObservableNumpyArray
  - ObservablePandasDataFrame
  - ObservableNamedTuple


>[!IMPORTANT]
> Other modules in pyggester are more specific and typically remain unchanged unless you're modifying the analysis approach. However, if you discover an improved method for analyzing or observing collections, or for the execution process post-code transformations, you're encouraged to submit a Pull Request (PR) with an explanation of your ideas. Please note that proposals involving substantial changes must be thoroughly documented, and test cases should be provided to demonstrate the advantages of your approach.


>[!NOTE]
>Additional examples can be found by reviewing the codebase directly, where docstrings provide a comprehensive understanding of Pyggester's architecture.




## Submitting Changes

1. **Commit Changes:** Commit your changes with a clear and concise commit message:

    ```bash
    git add .
    git commit -m "Brief description of your changes"
    ```

2. **Push Changes:** Push your changes to your forked repository:

    ```bash
    git push origin your-branch-name
    ```
3. **Open a Pull Request:** On GitHub, open a pull request from your branch to the main project repository. Provide a detailed description of your changes and any relevant information.