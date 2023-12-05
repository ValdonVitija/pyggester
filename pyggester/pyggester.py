import ast
import os
from typing import Dict, List, Any, Type, ClassVar, Set, Tuple
from pyggester.helpers import fetch_files
from pyggester.observable_collector import apply_observable_collector_transformations
import pathlib


# class PyggesterStatic:
#     """
#     Pyggester is a code analysis tool that processes and analyzes code files
#     based on specified analyzer categories.

#     Attributes:
#         analyzer_categories (AnalyzerCategories): The categories of analyzers available.
#         path_ (str): The path to the directory containing code files to analyze.
#         files_to_analyze (List[Tuple[str | pathlib.Path]]): List of file paths and corresponding code content.

#     """

#     def __init__(self, path_) -> None:
#         self.path_ = path_
#         self.files_to_analyze: List[Tuple[str | pathlib.Path]] = fetch_files(path=path_)

#     def run(self, categories_to_analyze) -> None:
#         """
#         This is the main function that initializes the process.
#         It loops through each collected file content/code, it creates a
#         tree abstraction representation of the code and runs the selected analyzers
#         """
#         for file_path, code_ in self.files_to_analyze:
#             tree = ast.parse(code_)
#             self.run_analyzers(
#                 categories_to_analyze=categories_to_analyze,
#                 tree=tree,
#                 file_path=file_path,
#             )

#     def run_analyzers(
#         self, categories_to_analyze: Set[str] | Tuple[str], tree, file_path
#     ) -> None:
#         """
#         Initialize and apply analyzers based on the type of data_structure.
#         Args:
#             data_structure: The data structure to be analyzed.
#         """

#         for category in categories_to_analyze:
#             for analyzer_model in getattr(self.analyzer_categories, category):
#                 analyzer = analyzer_model.Analyzer(file_path)
#                 analyzer.visit(tree)
#                 for message in analyzer_model.MessageIterator(analyzer):
#                     print(message)


class PyggesterDynamic:
    __slots__: Tuple[str] = "path_"

    def __init__(self, path_) -> None:
        self.path_ = path_

    def run(
        self,
    ) -> None:
        files = fetch_files(self.path_)
        print("AFTER FETCH FILES")
        print(files)
        for file_path, code in files:
            transformed_code = apply_observable_collector_transformations(
                ast.parse(code)
            )
            print("=" * 50)
            print(transformed_code)
            print("=" * 50)
            self.save_transformed_code(file_path, transformed_code)

    def save_transformed_code(self, original_path: pathlib.Path, code: str) -> None:
        print("INSIDE SAVE TRANSFORMED CODE")
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
        base_name, extension = os.path.splitext(original_path.name)
        new_base_name = f"{base_name}_transformed{extension}"
        return original_path.with_name(new_base_name)

    def get_unique_directory_path(self, original_path: pathlib.Path) -> pathlib.Path:
        new_dir_name = f"{original_path.name}_transformed"
        return original_path.parent / new_dir_name
