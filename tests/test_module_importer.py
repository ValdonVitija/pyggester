import ast
import unittest
import pytest
from pyggester.module_importer import (
    ImportsVisitor,
    ImportModuleTransformer,
    add_imports,
)
from pyggester.wrappers import get_wrappers_as_strings


class TestImportsVisitor(unittest.TestCase):
    def test_import_detection(self):
        code_import = "import module_name"
        self.assertTrue(self._check_import(code_import, "module_name"))

        code_import_alias = "import module_name as alias_name"
        self.assertTrue(self._check_import(code_import_alias, "module_name"))

        code_from_import = "from module_name import name1, name2"
        self.assertTrue(self._check_import(code_from_import, "module_name"))

        code_from_import_alias = (
            "from module_name import name1 as alias_name1, name2 as alias_name2"
        )
        self.assertTrue(self._check_import(code_from_import_alias, "module_name"))

        code_non_matching_import = "import other_module"
        self.assertFalse(self._check_import(code_non_matching_import, "module_name"))

        code_non_matching_from_import = "from other_module import name"
        self.assertFalse(
            self._check_import(code_non_matching_from_import, "module_name")
        )

    def _check_import(self, code, module_name):
        tree = ast.parse(code)
        visitor = ImportsVisitor(module_name, set())
        visitor.visit(tree)
        return visitor.imported


@pytest.mark.parametrize(
    "wrapper_name",
    [
        "ObservableListWrapper",
        "ObservableDictWrapper",
        "ObservableTupleWrapper",
        "ObservableSetWrapper",
        "ObservableNamedTupleWrapper",
        "ObservableNumpyArrayWrapper",
        "ObservablePandasDataFrameWrapper",
    ],
)
def test_import_addition(wrapper_name):
    code = "print('Hello, world!')"
    transformer = ImportModuleTransformer(
        ast.parse(code), "pyggester.wrappers", {wrapper_name}
    )
    transformed_code = _apply_transformer(transformer)

    assert wrapper_name in transformed_code
    assert "print('Hello, world!')" in transformed_code


@pytest.mark.parametrize(
    "wrapper_name",
    [
        "ObservableListWrapper",
        "ObservableDictWrapper",
        "ObservableTupleWrapper",
        "ObservableSetWrapper",
        "ObservableNamedTupleWrapper",
        "ObservableNumpyArrayWrapper",
        "ObservablePandasDataFrameWrapper",
    ],
)
def test_no_import_change(wrapper_name):
    code = f"from pyggester.wrappers import {wrapper_name}\nprint('Hello, world!')"
    transformer = ImportModuleTransformer(
        ast.parse(code), "pyggester.wrappers", {wrapper_name}
    )
    transformed_code = _apply_transformer(transformer)
    assert code in transformed_code


def _apply_transformer(transformer):
    transformed_tree = transformer.visit(transformer.tree_)
    return ast.unparse(transformed_tree)


@pytest.mark.parametrize(
    "wrapper_cls",
    [
        "ObservableListWrapper",
        "ObservableDictWrapper",
        "ObservableTupleWrapper",
        "ObservableSetWrapper",
        "ObservableNamedTupleWrapper",
        "ObservableNumpyArrayWrapper",
        "ObservablePandasDataFrameWrapper",
    ],
)
def test_add_imports(wrapper_cls):
    code = "print('Hello, world!')"
    tree = ast.parse(code)
    expected_code = f"from pyggester.observables import {wrapper_cls}\n{code}"
    transformed_tree = add_imports(tree, [wrapper_cls])
    assert ast.unparse(transformed_tree) == expected_code
