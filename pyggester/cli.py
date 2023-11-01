"""
This cli app is technically a composition of typer CLI apps.
The structure of this CLI app based on typer:
    app (typer):
        report (typer):
            generate OPTIONS
            inject OPTIONS
        device (typer):
            commands OPTIONS


If you need a command that contains subcommands, you have to declare it as a class that has an instance of the typer module
This means that you can compose typer instances with one another in a super scalable way.
For example:
    The App Class represents the root of this CLI app and it is a typer itself because it will contain other commands(subcommands).
    The Report Class is a typer on its own because it is a command(subcommand of app) that will contain other commands(subcommands).
    The Deivce Class is a typer on its own because it as a command(subcommand of app) that will contain other commands(subcommands).

Basically whenever you need to group commands within a command you create a class that represents a typer cli app on its own.
"""

from functools import lru_cache
from typing import List, Tuple
import typer
from typing_extensions import Annotated

__all__: List[str] = []

app = typer.Typer(no_args_is_help=True)
report_app = typer.Typer(no_args_is_help=True)
device_app = typer.Typer(no_args_is_help=True)


@device_app.command(no_args_is_help=True, name="inject")
def device_inject(
    database: Annotated[
        str, typer.Option("--database", help="Database connection string")
    ] = None,
    user: Annotated[str, typer.Option("--user", help="Database username")] = None,
    password: Annotated[
        str, typer.Option("--password", help="Database password")
    ] = None,
    node_query_file: Annotated[
        str,
        typer.Option("--node_query_file", help="Node query file to be injected"),
    ] = None,
    dir_path: Annotated[
        str,
        typer.Option(
            "--node_query_dir",
            help="Directory path to inject all the node query files that exist in it",
        ),
    ] = None,
    _id: Annotated[
        str,
        typer.Option(
            "--id",
            help="The id of the new document. This refers to the device name / CLLI",
        ),
    ] = None,
    NE_CATEGORY: Annotated[
        str,
        typer.Option(
            "--category",
            "--ne-category",
            "--NE_CATEGORY",
            help="Use this option to get the device category",
        ),
    ] = None,
    NE_SUBTYPE: Annotated[
        str,
        typer.Option(
            "--subtype",
            "--ne-subtype",
            "--NE_SUBTYPE",
            help="Use this option to get the subtype of device",
        ),
    ] = None,
    NE_Location_CLLI: Annotated[
        str,
        typer.Option(
            "--location",
            "--ne-location",
            "--NE_Location_CLLI",
            help="Use this option to get the device location",
        ),
    ] = None,
    NE_MGMT_IP: Annotated[
        str,
        typer.Option(
            "--ip",
            "--ip-address",
            "--ne-ip-address",
            "--NE_MGMT_IP",
            help="Use this option to get the device IP",
        ),
    ] = None,
    NE_VENDOR: Annotated[
        str,
        typer.Option(
            "--vendor",
            "--ne-vendor",
            "--NE_VENDOR",
            help="Use this option to get the device vendor",
        ),
    ] = None,
    NE_MODEL: Annotated[
        str,
        typer.Option(
            "--model",
            "--ne-model",
            "--NE_MODEL",
            help="Use this option to get the device model",
        ),
    ] = None,
    NE_SW_VERSION: Annotated[
        str,
        typer.Option(
            "--software-version",
            "--sv",
            "--sw-version",
            "--NE_SW_VERSION",
            help="Use this option to get the device software version",
        ),
    ] = None,
    GNE_ID: Annotated[str, typer.Option("--GNE_ID")] = None,
    GNE_MGMT_IP: Annotated[str, typer.Option("--GNE_MGMT_IP")] = None,
    NE_MOA: Annotated[
        str,
        typer.Option(
            "--moa",
            "--ne-moa",
            "--NE_MOA",
            help="Use this option to get the device moa",
        ),
    ] = None,
    NE_Description: Annotated[
        str,
        typer.Option(
            "--desc",
            "--description",
            "--ne-description",
            "--NE_Description",
            help="Use this option to get device description",
        ),
    ] = None,
    NE_SN: Annotated[str, typer.Option("--NE_SN")] = None,
    device_file: Annotated[
        str,
        typer.Option(
            "--device_file",
            help="Inject a new device based on a file that represents the device by key, value pairs(field=value)",
        ),
    ] = None,
    device_dir: Annotated[
        str,
        typer.Option(
            "--device_dir",
            help="Inject new devices based on a dir that contains files that represent devices by key, value pairs(field=value)",
        ),
    ] = None,
    HELP_: Annotated[
        bool, typer.Option("--HELP", help="Get full documentation")
    ] = False,
):
    pass
