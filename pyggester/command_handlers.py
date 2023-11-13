import abc
import os
import pathlib
import typer
from typing import Dict, List, ClassVar, Union
from rich.console import Console
from rich.markdown import Markdown
from enum import Enum, auto
from pyggester.text_formatters import custom_print
from pyggester.helpers import get_help_files_dir
from pyggester.pyggester import Pyggester

__all__: List[str] = ["PyggestStatic", "PyggestDynamic"]

README_FILES_DIR: pathlib.Path = get_help_files_dir()


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
        """
        Handle the --HELP option by displaying the README file.

        If the --HELP option is specified, this function reads and displays the README file
        using the Rich library's Console and Markdown features. It then raises a Typer Exit
        to terminate the program, because if the --HELP option gets used no other operation
        should take place

        Returns:
            Union[None, Exit]: None if the function doesn't return anything, or a Typer Exit object.
        """
        # pylint: disable=E1101
        if self.HELP_:
            console = Console()
            with open(os.path.join(README_FILES_DIR, self.README)) as readme:
                markdown = Markdown(readme.read())
                console.print(markdown)
                raise typer.Exit()

    def handle_no_valid_combination(self) -> Union[None, typer.Exit]:
        """
        Handle the case when there is no valid combination/usage of options.

        This function displays an error message using the custom_print function and raises
        a Typer Exit to terminate the program.
        """
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
        self.path_ = pathlib.Path(path_)
        self.LISTS_: bool = LISTS_
        self.DICTS_: bool = DICTS_
        self.SETS_: bool = SETS_
        self.TUPLES_: bool = TUPLES_
        self.all_: bool = all_
        self.HELP_: bool = HELP_
        self.README = pathlib.Path("static_helper.md")
        super().__init__()

    def process(self) -> None:
        try:
            pyggester = Pyggester(path_=self.path_)
            if self.HELP_:
                self.handle_HELP_()
            self.handle_all_standalone(pyggester)
            self.handle_chosen_categories(pyggester)
            self.handle_no_valid_combination()

        except Exception as ex:
            if isinstance(ex, typer.Exit):
                raise ex
            print(ex)

    def handle_chosen_categories(self, pyggester):
        if any([self.LISTS_, self.DICTS_, self.SETS_, self.TUPLES_]) and not self.all_:
            pyggester.run(self.categories_to_analyze())
            raise typer.Exit()

    def handle_all_standalone(self, pyggester):
        if self.all_ and not any(
            [[self.LISTS_, self.DICTS_, self.SETS_, self.TUPLES_]]
        ):
            pyggester.run(self.categories_to_analyze())
            raise typer.Exit()

    def categories_to_analyze(self):
        categories_ = set()
        if self.all_:
            return ("lists", "tuples", "sets", "dicts")

        if self.LISTS_:
            categories_.add("lists")
        if self.TUPLES_:
            categories_.add("tuples")
        if self.SETS_:
            categories_.add("sets")
        if self.DICTS_:
            categories_.add("dicts")

        return categories_


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
