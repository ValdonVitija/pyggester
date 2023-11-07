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
from pyggester.command_handlers import PyggestDynamic, PyggestStatic
from pyggester.helpers import not_implemented

__all__: List[str] = ["get_app"]

app = typer.Typer(no_args_is_help=True)


@app.command(no_args_is_help=True, name="static")
def static_analysis(
    path_: Annotated[
        str, typer.Option("--database", help="Database connection string")
    ] = None,
    LISTS_: Annotated[
        bool,
        typer.Option(
            "--lists",
            help="Use this option to include lists in analysis",
        ),
    ] = False,
    DICTS_: Annotated[
        bool,
        typer.Option(
            "--dicts",
            help="Use this option to include dicts in analysis",
        ),
    ] = False,
    SETS_: Annotated[
        bool,
        typer.Option(
            "--sets",
            help="Use this option to include sets in analysis",
        ),
    ] = False,
    TUPLES_: Annotated[
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
            help="If you want pyggester to use all its capabilites use this option",
        ),
    ] = False,
    HELP_: Annotated[
        bool, typer.Option("--HELP", help="Get full documentation")
    ] = False,
):
    """
    NOTE: This function represents the 'static' subcommand of pyggest

    Perform static analysis using PyggestStatic.

    This command allows you to perform static analysis using PyggestStatic, a tool for
    analyzing Python code. You can specify various options to customize the analysis.

    Args:
        path_ (str): Database connection string.
        LISTS_ (bool): Whether to include lists in the analysis.
        DICTS_ (bool): Whether to include dicts in the analysis.
        SETS_ (bool): Whether to include sets in the analysis.
        TUPLES_ (bool): Whether to include tuples in the analysis.
        all_ (bool): If True, use all available analysis capabilities.
        HELP_ (bool): If True, get full documentation.

    Returns:
        None
    """
    command_handler = PyggestStatic(
        path_=path_,
        LISTS_=LISTS_,
        DICTS_=DICTS_,
        SETS_=SETS_,
        TUPLES_=TUPLES_,
        all_=all_,
        HELP_=HELP_,
    )
    command_handler.process()


@not_implemented
@app.command(no_args_is_help=True, name="dynamic")
def dynamic_analysis():
    """
    Perform dynamic analysis using PyggestDynamic.

    This command allows you to perform dynamic analysis using PyggestDynamic, a tool for
    analyzing Python code at runtime.

    Args:
        ...

    Returns:
        None
    """
    command_handler = PyggestDynamic()
    command_handler.process()


@lru_cache
def get_app():
    return app()
