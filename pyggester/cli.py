"""
The structure of this CLI app based on typer:
    app (typer) - pyggest:
        static - subcommand:
            Options: ...
        dynamic - subcommand
            Options: ...
"""

from functools import lru_cache
from typing import List
import typer
from typing_extensions import Annotated
from pyggester.command_handlers import PyggestTransform
from pyggester.helpers import not_implemented

__all__: List[str] = ["get_app"]

app = typer.Typer(no_args_is_help=True)


# pylint: disable=W0613
@app.command(no_args_is_help=False, name="static")
def static_analysis(
    path_: Annotated[str, typer.Option("--path", help="path to file/files")] = None,
    lists_: Annotated[
        bool,
        typer.Option(
            "--lists",
            help="Use this option to include lists in analysis",
        ),
    ] = False,
    dicts_: Annotated[
        bool,
        typer.Option(
            "--dicts",
            help="Use this option to include dicts in analysis",
        ),
    ] = False,
    sets_: Annotated[
        bool,
        typer.Option(
            "--sets",
            help="Use this option to include sets in analysis",
        ),
    ] = False,
    tuples_: Annotated[
        bool,
        typer.Option(
            "--tuples",
            help="Use this option to include tuples in analysis",
        ),
    ] = False,
    all_: Annotated[
        bool,
        typer.Option(
            "--all",
            help="If you want pyggester to use all its capabilities use this option",
        ),
    ] = False,
    help_: Annotated[
        bool, typer.Option("--help", help="Get full documentation")
    ] = False,
):
    """
    Perform static analysis using PyggestStatic.

    This command allows you to perform static analysis using PyggestStatic, a tool for
    analyzing Python code. You can specify various options to customize the analysis.

    """
    typer.Exit("Not implemented currently.")


@app.command(no_args_is_help=True, name="transform")
def dynamic_transformation(
    path_: Annotated[str, typer.Argument(help="path to file/files")] = ".",
    help_: Annotated[
        bool, typer.Option("--help", help="Get full documentation")
    ] = False,
):
    """
    Perform dynamic transformation using PyggesterDynamic.
    """
    command_handler = PyggestTransform(path_=path_, help_=help_)
    command_handler.process()


@lru_cache
def get_app():
    """
    Get the main typer cli app
    """
    return app()
