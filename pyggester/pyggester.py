import ast
import os
from typing import Dict, List, Any, Type, ClassVar, Set, Tuple, Union

from pyggester.observable_transformations import (
    apply_observable_collector_transformations,
)
import pathlib


class PyggesterDynamic:
    """
    A class that represents the dynamic behavior of Pyggester.

    PyggesterDynamic is responsible for executing the transformation process based on the provided path.
    It determines whether to transform a single file or multiple files based on the number of files found in the path.
    If only one file is found, it will be transformed with observables enabled.
    If multiple files are found, the user will be prompted to input the main file name for application execution.
    The main file will be transformed with observables enabled, while the rest of the files will be transformed without observables.

    """

    __slots__: Tuple[str] = "path_"

    def __init__(self, path_) -> None:
        self.path_ = path_

    def run(self) -> None:
        """
        Executes the transformation process based on the provided path.

        If only one file is found in the path, it will be transformed with observables enabled.
        If multiple files are found, the user will be prompted to input the main file name for application execution.
        The main file will be transformed with observables enabled, while the rest of the files will be transformed without observables.

        Raises:
            Exception: If the user input for the main file path is not a valid string.
        """
        files = self.fetch_files(self.path_)

        if len(files) == 1:
            self.transform_as(files[0], files[-1], run_observables=True)
        else:
            try:
                main_file_input = str(
                    input(
                        "Path detected as directory. Input the file name of your main entry point of application execution: "
                    )
                )
                main_file = pathlib.Path(main_file_input).absolute()
                for file_path, code in files:
                    if file_path == main_file:
                        self.transform_as(file_path, code, run_observables=True)
                    else:
                        self.transform_as(file_path, code)

            except Exception as _:
                print(
                    "Requested a string to represent the path to the main file of your application, got something else. Aborting."
                )

    def fetch_files(self, path: Union[str, None]) -> List[Tuple[str | pathlib.Path]]:
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
        ret_files: List[Tuple[str | pathlib.Path]] = []
        path = pathlib.Path(path).absolute() if path else pathlib.Path(".")

        if path.is_file() and path.suffix == ".py":
            self.save_file_content_as_str_(path, ret_files)

        elif path.is_dir():
            for root, _, files in os.walk(path):
                for file in files:
                    file_path = pathlib.Path(os.path.join(root, file))
                    if file_path.suffix == ".py":
                        self.save_file_content_as_str_(file_path, ret_files)

        return ret_files

    def save_file_content_as_str_(
        self, file_path: pathlib.Path, ret_files: List[Tuple[str | pathlib.Path]]
    ) -> None:
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
                ret_files.append((file_path, code__))

        except FileNotFoundError as err__:
            print(err__)

    def transform_as(self, file_path, code, run_observables=False):
        """
        Transforms the given code using observable collector transformations and saves the transformed code to a file.

        Args:
            file_path (str): The path of the file to save the transformed code.
            code (str): The code to be transformed.
            run_observables (bool, optional): Whether to run observables during the transformation. Defaults to False.
        """
        transformed_code = apply_observable_collector_transformations(
            ast.parse(code), run_observables=run_observables
        )
        self.save_transformed_code(file_path, transformed_code)

    def save_transformed_code(self, original_path: pathlib.Path, code: str) -> None:
        """
        Save the transformed code to a new file or directory.

        Args:
            original_path (pathlib.Path): The path to the original file or directory.
            code (str): The transformed code to be saved.

        Returns:
            None

        Raises:
            FileNotFoundError: If the original_path does not exist.
            IsADirectoryError: If the original_path is a file and not a directory.

        Algorithm:
            1. If original_path is a file:
                - Get a unique file path using the get_unique_file_path method.
                - Open the new file path in write mode.
                - Write the transformed code to the file.
            2. If original_path is a directory:
                - Get a unique directory path using the get_unique_directory_path method.
                - Create the new directory path if it doesn't exist.
                - Traverse the original directory using os.walk.
                - For each file in the directory:
                    - Read the original code from the file.
                    - Apply observable collector transformations to the original code.
                    - Get the relative path of the file with respect to the original directory.
                    - Create the new file path by joining the new directory path and the relative path.
                    - Open the new file path in write mode.
                    - Write the transformed code to the file.
        """
        if original_path.is_file():
            new_file_path = self.get_unique_file_path(original_path)
            with open(new_file_path, "w", encoding="UTF-8", errors="ignore") as f:
                f.write(code)
        elif original_path.is_dir():
            new_dir_path = self.get_unique_directory_path(original_path)
            os.makedirs(new_dir_path, exist_ok=True)
            for root, _, files in os.walk(original_path):
                for file in files:
                    file_path = pathlib.Path(os.path.join(root, file))
                    with open(file_path, "r", encoding="UTF-8", errors="ignore") as f:
                        original_code = f.read()
                    transformed_code = apply_observable_collector_transformations(
                        original_code
                    )
                    relative_path = file_path.relative_to(original_path)
                    new_file_path = os.path.join(new_dir_path, relative_path)
                    with open(
                        new_file_path, "w", encoding="UTF-8", errors="ignore"
                    ) as f:
                        f.write(transformed_code)

    def get_unique_file_path(self, original_path: pathlib.Path) -> pathlib.Path:
        """
        Returns a unique file path by appending '_transformed' to the base name of the original file path.

        Args:
            original_path (pathlib.Path): The original file path.

        Returns:
            pathlib.Path: The unique file path.
        """
        base_name, extension = os.path.splitext(original_path.name)
        new_base_name = f"{base_name}_transformed{extension}"
        return original_path.with_name(new_base_name)

    def get_unique_directory_path(self, original_path: pathlib.Path) -> pathlib.Path:
        """
        Returns a unique directory path by appending '_transformed' to the original directory name.

        Args:
            original_path (pathlib.Path): The original directory path.

        Returns:
            pathlib.Path: The unique directory path.
        """
        new_dir_name = f"{original_path.name}_transformed"
        return original_path.parent / new_dir_name
