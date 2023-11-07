import pathlib
import os
from typing import List, Union
import ast


def fetch_files(path: Union[str, None]) -> List[str]:
    """
    This helper function fetches the content of Python files to be analyzed by pyggester.

    Args:
        path (str | None): The path to the Python file or directory to analyze.
            If 'None', it assumes you want to analyze the entire directory structure
            from the directory where pyggester is running. If a specific file is provided,
            it fetches the content of that file (assuming it is a Python file), otherwise,
            an error occurs. If the given path is a directory, it recursively analyzes
            all the files in all directories and subdirectories within the provided directory.

    Returns:
        List[str]: A list of the content of Python files to be analyzed.
    """
    ret_files: List[str] = []
    path = pathlib.Path(path) if path else pathlib.Path(".")

    if path.is_file() and path.suffix == ".py":
        save_file_content_as_str_(path, ret_files)

    elif path.is_dir():
        for root, _, files in os.walk(path):
            for file in files:
                file_path = pathlib.Path(os.path.join(root, file))
                if file_path.suffix == ".py":
                    save_file_content_as_str_(file_path, ret_files)

    return ret_files


def save_file_content_as_str_(file_path: pathlib.Path, ret_files: List[str]) -> None:
    """
    Reads the content of a file and appends it to a list of strings.

    Args:
        file_path (pathlib.Path): The path to the file to be read.
        ret_files (List[str]): A list to which the file's content will be appended.

    This function is used to save the content of each file as a string. The purpose is to prepare
    the content for parsing with the `ast` module, which expects input as a multiline string
    separated by newline characters.
    """
    try:
        with open(file_path, "r", encoding="UTF-8", errors="ignore") as f_stream:
            code__ = f_stream.read()
            ret_files.append(code__)

    except FileNotFoundError as err__:
        print(err__)


if __name__ == "__main__":
    files = fetch_files("main.py")
    for code in files:
        tree = ast.parse(code)
        print(ast.dump(tree, indent=4))
