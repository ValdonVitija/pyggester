import abc
import os
import pathlib
import typer
from typing import Dict, List, ClassVar, Union
from rich.console import Console
from rich.markdown import Markdown
from pyggester.text_formatters import custom_print

__all__: List[str] = ["PyggestStatic", "PyggestDynamic"]

README_FILES_DIR: type[pathlib.Path] = pathlib.Path(
    os.path.join(
        pathlib.Path(__file__).parent,
        "data",
        "help_files",
    )
)


class CommandHandler(abc.ABC):
    """
    Template command handler.
    Add as many methods in the classes that derive from this base handler as you need.
    If each command only needed a single function to process the logic this design pattern
    wouldn't be necesseary. The main reason why each handler is a class it is beacause classes
    can act like namespaces, so we can have same function names and variable names under a different namespace(class)
    """

    @abc.abstractmethod
    def process(self) -> None:
        ...

    def handle_HELP_(self) -> Union[None, typer.Exit]:
        if self.HELP_:
            console = Console()
            with open(os.path.join(README_FILES_DIR, self.README)) as readme:
                markdown = Markdown(readme.read())
                console.print(markdown)
                raise typer.Exit()

    def handle_no_valid_combination(self) -> Union[None, typer.Exit]:
        custom_print(
            "No valid combination/usage of options! Try --help or --HELP",
            border_style="red",
            title="EXIT INFO",
        )
        raise typer.Exit()


class PyggestStatic(CommandHandler):
    """
    This class handles the variations of options supported under:
        pyggest static
    """

    __slots__: ClassVar[List[str]] = [
        "path_",
        "LISTS_",
        "DICTS_",
        "SETS_",
        "TUPLES_",
        "all_",
        "HELP_",
    ]

    def __init__(
        self,
        path_: pathlib.Path,
        LISTS_: bool,
        DICTS_: bool,
        SETS_: bool,
        TUPLES_: bool,
        all_: bool,
        HELP_: bool,
    ) -> None:
        self.path_: pathlib.Path = pathlib.Path(path_)
        self.LISTS_: bool = LISTS_
        self.DICTS_: bool = DICTS_
        self.SETS_: bool = SETS_
        self.TUPLES_: bool = TUPLES_
        self.all_: bool = all_
        self.HELP_: bool = HELP_
        self.README = pathlib.Path("static_helper.md")
        super().__init__()

    def process(self) -> None:
        pass


class PyggestDynamic(CommandHandler):
    """
    This class handles the variations of options supported under:
        pyggest dynamic
    """

    __slots__: ClassVar[List[str]] = []

    def __init__(self) -> None:
        self.README = pathlib.Path("dynamic_helper.md")
        super().__init__()

    def process(self) -> None:
        pass
