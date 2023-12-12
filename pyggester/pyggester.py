import ast
import os
import shutil
from typing import List, Tuple
import pathlib
from pyggester.observable_transformations import (
    apply_observable_collector_transformations,
)


class PyggesterDynamic:
    def __init__(self, path_: str) -> None:
        self.path_ = pathlib.Path(path_).absolute()

    def run(self):
        if not self.path_.exists():
            raise FileNotFoundError(f"The path '{self.path_}' does not exist.")

        if self.path_.is_file():
            self._transform_file(self.path_, run_observable=True)
        elif self.path_.is_dir():
            self._transform_directory()

    def _transform_file(self, file_path: pathlib.Path, run_observable: bool) -> None:
        code = file_path.read_text(encoding="UTF-8")
        transformed_code = apply_observable_collector_transformations(
            ast.parse(code), run_observables=run_observable
        )
        transformed_file_path = (
            file_path.parent / f"{file_path.stem}_transformed{file_path.suffix}"
        )
        transformed_file_path.write_text(transformed_code, encoding="UTF-8")

    def _transform_directory(self) -> None:
        main_file_name = input("Enter the name of the main file: ")
        main_file_path = self.path_ / main_file_name

        if not main_file_path.exists():
            raise FileNotFoundError(f"The main file '{main_file_path}' does not exist.")

        transformed_dir_path = self.path_.parent / f"{self.path_.name}_transformed"
        os.makedirs(transformed_dir_path, exist_ok=True)

        for root, dirs, files in os.walk(self.path_):
            for dir_name in dirs:
                os.makedirs(transformed_dir_path / dir_name, exist_ok=True)
            for file_name in files:
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
