import sys
from pyggester.cli import get_app
from rich.console import Console
from rich.markdown import Markdown
import os
import pathlib


PYGGESTER_LOGO = """
"""


def main():
    args = " ".join(sys.argv[1:])
    if (not args or "--help" in args) and len(sys.argv) < 3:
        print(PYGGESTER_LOGO)
    get_app()


if __name__ == "__main__":
    main()
