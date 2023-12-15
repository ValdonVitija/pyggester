import ast
import os
import shutil
from typing import List, Tuple
import pathlib
from pyggester.observable_transformations import (
    apply_observable_collector_transformations,
)
from pyggester.text_formatters import custom_print


class PyggesterDynamic:
    """
    A class for dynamically transforming files / directories
    This is the main 'engine' that glues everything together for pyggester to work under 'pyggester transform'

    Args:
        path_ (str): The path to the file or directory to be transformed.

    Attributes:
        path_ (pathlib.Path): The absolute path to the file or directory.

    Methods:
        run(): Runs the transformation process based on the type of path provided.
        _transform_file(file_path, run_observable): Transforms a single file.
        _transform_directory(): Transforms all files in a directory.
    """

    __slots__ = ("path_",)

    def __init__(self, path_: str) -> None:
        self.path_ = pathlib.Path(path_).absolute()

    def run(self):
        """
        Runs the transformation process based on the type of path provided.
        """
        if not self.path_.exists():
            raise FileNotFoundError(f"The path '{self.path_}' does not exist.")

        if self.path_.is_file():
            self._transform_file(self.path_, run_observable=True)
            custom_print("File transformed successfully!", border_style="green")
        elif self.path_.is_dir():
            self._transform_directory()
            custom_print("Directory transformed successfully!", border_style="green")

    def _transform_file(self, file_path: pathlib.Path, run_observable: bool) -> None:
        """
        Transforms a single file by applying observable collector transformations.

        This method reads the content of the specified file, applies observable collector transformations
        to the abstract syntax tree (AST) representation of the code, and writes the transformed code
        to a new file.

        The observable collector transformations include analyzing and modifying the AST to collect
        observables and perform any necessary transformations based on the `run_observable` flag.

        Args:
            file_path (pathlib.Path): The path to the file to be transformed.
            run_observable (bool): Indicates whether to run observables in the file.

        Returns:
            None
        """
        code = file_path.read_text()
        transformed_code = apply_observable_collector_transformations(
            ast.parse(code), run_observables=run_observable
        )
        transformed_file_path = (
            file_path.parent / f"{file_path.stem}_transformed{file_path.suffix}"
        )
        transformed_file_path.write_text(transformed_code)

    def _transform_directory(self) -> None:
        """
        Transforms all files in a directory.

        This method takes the name of the main file as input and transforms all the files in the directory
        specified by `self.path_`. It creates a new directory named "{self.path_.name}_transformed" in the
        parent directory of `self.path_` to store the transformed files.

        For each file in the directory, it checks if the file path matches the main file path. If it does,
        the file is considered as the main file and is transformed with the `run_observable` flag set to True.
        Otherwise, the file is transformed with the `run_observable` flag set to False.

        The transformed file is then moved to the corresponding location in the transformed directory, while
        preserving the directory structure.

        Args:
            None

        Returns:
            None
        """
        main_file_name = input("Enter the name of the main file: ")
        main_file_path = self.path_ / main_file_name

        if not main_file_path.exists():
            raise FileNotFoundError(f"The main file '{main_file_path}' does not exist.")

        transformed_dir_path = self.path_.parent / f"{self.path_.name}_transformed"
        os.makedirs(transformed_dir_path, exist_ok=True)

        excluded_dirs = {"__pycache__", ".git", ".venv"}

        for root, dirs, files in os.walk(self.path_):
            dirs[:] = [d for d in dirs if d not in excluded_dirs]
            for dir_name in dirs:
                os.makedirs(transformed_dir_path / dir_name, exist_ok=True)
            for file_name in files:
                if file_name.endswith(".py"):
                    file_path = pathlib.Path(root) / file_name
                    run_observable = file_path == main_file_path
                    self._transform_file(file_path, run_observable=run_observable)

                    relative_path = file_path.relative_to(self.path_)
                    transformed_file_path = transformed_dir_path / relative_path
                    transformed_file_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(
                        file_path.with_name(
                            f"{file_path.stem}_transformed{file_path.suffix}"
                        ),
                        transformed_file_path,
                    )
                else:
                    file_path = pathlib.Path(root) / file_name
                    relative_path = file_path.relative_to(self.path_)
                    transformed_file_path = transformed_dir_path / relative_path
                    transformed_file_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy(
                        file_path,
                        transformed_file_path,
                    )
