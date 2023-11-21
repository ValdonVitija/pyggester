import abc
import os
import pathlib
import typer
from typing import Dict, List, ClassVar, Union, Tuple
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

    def handle_help_(self) -> Union[None, typer.Exit]:
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

    __slots__: ClassVar[Tuple[str]] = (
        "path_",
        "lists_",
        "dicts_",
        "sets_",
        "tuples_",
        "all_",
        "help_",
    )

    def __init__(
        self,
        path_: pathlib.Path,
        lists_: bool,
        dicts_: bool,
        sets_: bool,
        tuples_: bool,
        all_: bool,
        help_: bool,
    ) -> None:
        self.path_ = pathlib.Path(path_)
        self.lists_: bool = lists_
        self.dicts_: bool = dicts_
        self.sets_: bool = sets_
        self.tuples_: bool = tuples_
        self.all_: bool = all_
        self.help_: bool = help_
        self.README = pathlib.Path("static_helper.md")
        super().__init__()

    def process(self) -> None:
        try:
            pyggester = Pyggester(path_=self.path_)
            if self.help_:
                self.handle_help_()
            self.handle_all_standalone(pyggester)
            self.handle_chosen_categories(pyggester)
            self.handle_no_valid_combination()

        except Exception as ex:
            if isinstance(ex, typer.Exit):
                raise ex
            print(ex)

    def handle_chosen_categories(self, pyggester):
        if any([self.lists_, self.dicts_, self.sets_, self.tuples_]) and not self.all_:
            pyggester.run(self.categories_to_analyze())
            raise typer.Exit()

    def handle_all_standalone(self, pyggester):
        if self.all_ and not any(
            [[self.lists_, self.dicts_, self.sets_, self.tuples_]]
        ):
            pyggester.run(self.categories_to_analyze())
            raise typer.Exit()

    def categories_to_analyze(self):
        categories_ = set()
        if self.all_:
            return ("lists", "tuples", "sets", "dicts")

        if self.lists_:
            categories_.add("lists")
        if self.tuples_:
            categories_.add("tuples")
        if self.sets_:
            categories_.add("sets")
        if self.dicts_:
            categories_.add("dicts")

        return categories_


class PyggestDynamic(CommandHandler):
    """
    This class handles the variations of options supported under:
        pyggest dynamic
    """

    __slots__: ClassVar[tuple[str]] = ()

    def __init__(self) -> None:
        self.README = pathlib.Path("dynamic_helper.md")
        super().__init__()

    def process(self) -> None:
        pass
