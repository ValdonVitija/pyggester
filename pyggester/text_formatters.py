from rich.console import Console
from rich.panel import Panel


def custom_print(
    message: str = "",
    style: str = "bold",
    border_style: str = "",
    title: str = "",
):
    if message:
        panel_ = Panel(
            f"[bold yellow]{message}",
            style=style,
            border_style=border_style,
            title=title,
        )
        Console().print(panel_)
