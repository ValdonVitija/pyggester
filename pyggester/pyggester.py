import ast
from typing import Dict, List, Any, Type, ClassVar, Set, Tuple
from pyggester.analyzer_iterator_mapping import (
    get_analyzer_categories,
    AnalyzerCategories,
)
from pyggester.helpers import fetch_files
import pathlib


class Pyggester:
    """
    Pyggester is a code analysis tool that processes and analyzes code files
    based on specified analyzer categories.

    Attributes:
        analyzer_categories (AnalyzerCategories): The categories of analyzers available.
        path_ (str): The path to the directory containing code files to analyze.
        files_to_analyze (List[Tuple[str | pathlib.Path]]): List of file paths and corresponding code content.

    """

    def __init__(self, path_) -> None:
        self.analyzer_categories: AnalyzerCategories = get_analyzer_categories()
        self.path_ = path_
        self.files_to_analyze: List[Tuple[str | pathlib.Path]] = fetch_files(path=path_)

    def run(self, categories_to_analyze) -> None:
        """
        This is the main function that initializes the process.
        It loops through each collected file content/code, it creates a
        tree abstraction representation of the code and runs the selected analyzers
        """
        for file_path, code_ in self.files_to_analyze:
            tree = ast.parse(code_)
            self.run_analyzers(
                categories_to_analyze=categories_to_analyze,
                tree=tree,
                file_path=file_path,
            )

    def run_analyzers(
        self, categories_to_analyze: Set[str] | Tuple[str], tree, file_path
    ) -> None:
        """
        Initialize and apply analyzers based on the type of data_structure.
        Args:
            data_structure: The data structure to be analyzed.
        """

        for category in categories_to_analyze:
            for analyzer_model in getattr(self.analyzer_categories, category):
                analyzer = analyzer_model.Analyzer(file_path)
                analyzer.visit(tree)
                for message in analyzer_model.MessageIterator(analyzer):
                    print(message)
