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
from pyggester.pyggester import PyggesterDynamic

__all__: List[str] = ["PyggestTransform"]

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
        if self.help_:
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


class PyggestTransform(CommandHandler):
    """
    This class handles the variations of options supported under:
        pyggest dynamic
    """

    __slots__: ClassVar[tuple[str]] = "path_", "help_"

    def __init__(self, path_, help_) -> None:
        self.README = pathlib.Path("dynamic_helper.md")
        self.path_ = path_
        self.help_ = help_

        super().__init__()

    def process(self) -> None:
        try:
            if self.help_:
                self.handle_help_()
            pyggester = PyggesterDynamic(self.path_)
            pyggester.run()

        except Exception as ex:
            if isinstance(ex, typer.Exit):
                raise ex
            print(ex)
