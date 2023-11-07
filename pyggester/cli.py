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

__all__: List[str] = ["get_app"]

app = typer.Typer(no_args_is_help=True)

"""
    The following function represents the 'static' subcommand.
    If you need to add more options under this subcommand,
    just add another parameter in the end, but make sure 
    to handle that option properly
"""


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


"""
    The following function represents the 'dynamic' subcommand.
    If you need to add more options under this subcommand,
    just add another parameter in the end, but make sure 
    to handle that option properly
"""


@app.command(no_args_is_help=True, name="dynamic")
def dynamic_analysis():
    command_handler = PyggestDynamic()
    command_handler.process()


@lru_cache
def get_app():
    return app()
