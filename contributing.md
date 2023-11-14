# Welcome to pyggester!

Thank you for your interest in contributing to pyggester. Whether you're a developer, designer, tester, or someone with great ideas, your contributions are valuable.

## Getting Started

1. **Fork the Repository:** Start by forking the [Project Repository](link-to-repo) on GitHub. This creates a copy of the project under your GitHub account.

    ```bash
    git clone https://github.com/your-username/project-name.git
    ```

2. **Create a Branch:** Move into the project's directory and create a new branch for your contribution:

    ```bash
    cd pyggester
    git checkout -b your-branch-name
    ```

## Making Changes

Changes can encompass various aspects, provided they are reasonable. We welcome modifications to overall logic, naming conventions, hierarchy, and directory structure (with meticulous attention, especially for alterations to the project directory, requiring extreme detail).

### Adding new analyzers

The current design offers a good template for new analyzers. We have a base abstract class (`Analyzer`) that needs to be derived, while also deriving from `ast.NodeVisitor`.

#### `Analyzer` - Abstract Class

```python
class Analyzer(abc.ABC):
    """
    Abstract base class for data structure analyzers.
    ... (rest of the docstring)
    """
    def __init__(self, pathconfig: PathConfig):
        self.structures__: Dict[str, Dict[str, Union[str, int, bool]]] = {}
        self.pathconfig: PathConfig = pathconfig
```
A new analyzer typically needs to define a series of visitor methods starting from visit_Module.

```python
def visit_Module(self, node: ast.Module) -> Any:
        self.generic_visit(node)
```
The Visit Module is designed to initiate analysis from the top-level construct within the file. Further, integrate additional visitor methods to systematically traverse each essential node during the analysis process.

Organize the logic within the visitor methods and other custom functions to improve the code's readability within the analyzer. Make certain to populate the data structure, 'structures__', with distinct keys and corresponding values. This facilitates later interpretation of any identified suggestions.

Illustrative Example:

```python
def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        self.pathconfig.current_class: str = node.name
        self.generic_visit(node)
```

This class performs the same operations as the visit_Module, specifically focusing on Class nodes. Additionally, it updates the value of self.pathconfig.current_class, enabling the tracking of the currently analyzed class. This tracking is crucial, as the entire path from the root_file to the most specific scope serves as a key to uniquely identify each Python data structure encountered.

Continue extending this class by incorporating additional visitor methods to systematically explore each required node in the analysis.

Organize the logic within the visitor methods and other custom functions to enhance the overall readability of the code within the analyzer. Ensure that the structures__ data structure is populated with specific keys and values, facilitating the interpretation of any identified suggestions at a later stage.

For instance:

```python
class TupleInsteadOfListAnalyzer(Analyzer, ast.NodeVisitor):
    __slots__: ClassVar[Set[str]] = {
        "structures__",
        "pathconfig"
    }

    def __init__(self, current_module):
        super().__init__(
            pathconfig=PathConfig(current_module=current_module),
        )

    def visit_Module(self, node: ast.Module) -> Any:
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        self.pathconfig.current_class: str = node.name
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        self.pathconfig.current_function: str = node.name
        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> Any:
        self.generic_visit(node)

    def visit_While(self, node: ast.While) -> Any:
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> Any:
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
```
The TupleInsteadOfListAnalyzer serves the specific purpose of recommending the utilization of a tuple instead of a list. This suggestion applies when a list has been declared with a fixed set of values and remains unchanged throughout its existence.

Once all the necessary tasks within the analyzer are complete, the next step is to develop a message iterator specifically for this analyzer. Each message iterator should inherit from a base abstract class called MessageIterator.

#### `MessageIterator`
```python
class MessageIterator:
    """ """

    def __init__(self, analyzer: Analyzer, message: str) -> None:
        self.analyzer = analyzer
        self.message: str = message

    def __iter__(self) -> Set[str] | NotImplementedError:
        raise NotImplementedError
```
An actual instance of a message iterator is the `TupleInsteadOfListAnalyzerMessageIterator.`

```python
class TupleInsteadOfListAnalyzerMessageIterator(MessageIterator):
    """
    Message interpreter for tuple instead of list analyzer
    """

    __slots__: ClassVar[Set[str]] = ["analyzer"]

    def __init__(self, analyzer: Analyzer) -> None:
        super().__init__(analyzer, "USE A TUPLE INSTEAD OF A LIST")

    def __iter__(self):
        report__ = set()
        for _, value in self.analyzer.structures__.items():
            if not value["modified"]:
                report__.add(f"Line nr: {value['line_nr']} | {self.message}")

        return iter(report__)
```

This design establishes a direct correlation between the analyzer and the corresponding message iterator.

In the final step, once the analyzer and message iterator are both completed, the next task is to associate them. This association is performed within the file analyzer_iterator_mapping.py.

Within this file, a Pydantic model is provided, offering a structured way to map each analyzer with its respective message iterator. As each analyzer belongs to a specific group or category, navigate to the MODEL dictionary and include your newly created analyzer. Ensure that you instantiate a new AnalyzerModel object, using the analyzer and message iterator as parameter values. No further changes are necessary for Pyggester to function correctly, as the remaining procedures have been abstracted adequately. 
>[!IMPORTANT]
>If you discover a more efficient way to construct analyzers, with benefits in memory usage, computational speed, and code readability, document the process thoroughly, create a pull request, and, if deemed reasonable, we may embark on a significant refactoring phase for all existing analyzers. The goal is to optimize this project to its fullest extent.


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