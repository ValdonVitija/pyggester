import pathlib
import os
from functools import lru_cache


@lru_cache
def get_help_files_dir() -> pathlib.Path:
    """
    Get the directory path where help files are located.

    This function returns the directory path as a pathlib.Path object.
    The directory is determined relative to the location of the current script.

    Returns:
        pathlib.Path: The directory path for help files.
    """
    help_files_dir = pathlib.Path(
        os.path.join(
            pathlib.Path(__file__).parent,
            "data",
            "help_files",
        )
    )
    return help_files_dir


class PathMissingSourceCodeConversionError(Exception):
    """
    Exception Class to be thrown when path misses for source code conversion to str
    """

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def source_code_to_str(path=None) -> str:
    """
    Convert module source_code to a multiline string.
    By default it converts the source code of the module where this function is being called
    """
    if not path:
        raise PathMissingSourceCodeConversionError()

    with open(path, "r", encoding="UTF-8") as f_stream:
        return f_stream.read()


def not_implemented(func):
    """
    Decorator to flag a function as not yet implemented.

    This decorator raises a NotImplementedError when the decorated function is called,
    indicating that the function is not yet fully implemented.

    Args:
        func (callable): The function to be decorated.

    Returns:
        callable: A wrapper function that raises a NotImplementedError.
    """

    def wrapper(*args, **kwargs):
        raise NotImplementedError(f"{func.__name__} is not yet implemented")

    return wrapper
