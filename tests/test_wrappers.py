# pylint: disable=W0611
import ast
import pytest
from pyggester.wrappers import (
    ObservableListWrapper,
    ObservableDictWrapper,
    ObservableTupleWrapper,
    ObservableSetWrapper,
    ObservableNamedTupleWrapper,
    ObservableNumpyArrayWrapper,  # noqa: F401
    ObservablePandasDataFrameWrapper,  # noqa: F401
)

from pyggester.observables import (
    ObservableDict,  # noqa: F401
    ObservableList,  # noqa: F401
    ObservableNamedTuple,  # noqa: F401
    ObservableNumpyArray,  # noqa: F401
    ObservablePandasDataFrame,  # noqa: F401
    ObservableTuple,  # noqa: F401
    ObservableSet,  # noqa: F401
)


@pytest.fixture
def example_list_node():
    return ast.parse("[1, 2, 3]").body[0].value


@pytest.fixture
def example_dict_node():
    return ast.parse("{1: 'one', 2: 'two'}").body[0].value


@pytest.fixture
def example_tuple_node():
    return ast.parse("(1, 2, 3)").body[0].value


@pytest.fixture
def example_set_node():
    return ast.parse("{1, 2, 3}").body[0].value


def test_observable_list_wrapper(example_list_node):
    transformer = ObservableListWrapper()
    transformed_node = transformer.visit(example_list_node)
    assert isinstance(transformed_node, ast.Call)
    assert ast.unparse(transformed_node) == "ObservableList([1, 2, 3])"


def test_observable_dict_wrapper(example_dict_node):
    transformer = ObservableDictWrapper()
    transformed_node = transformer.visit(example_dict_node)
    assert isinstance(transformed_node, ast.Call)
    assert ast.unparse(transformed_node) == "ObservableDict({1: 'one', 2: 'two'})"


def test_observable_tuple_wrapper(example_tuple_node):
    transformer = ObservableTupleWrapper()
    transformed_node = transformer.visit(example_tuple_node)
    assert isinstance(transformed_node, ast.Call)
    assert ast.unparse(transformed_node) == "ObservableTuple((1, 2, 3))"


def test_observable_set_wrapper(example_set_node):
    transformer = ObservableSetWrapper()
    transformed_node = transformer.visit(example_set_node)
    assert isinstance(transformed_node, ast.Call)
    assert ast.unparse(transformed_node) == "ObservableSet({1, 2, 3})"


class TestObservableNamedTupleWrapper:
    @staticmethod
    def transform_and_get_code(code):
        tree = ast.parse(code)
        transformer = ObservableNamedTupleWrapper(tree)
        transformed_tree = transformer.visit(tree)
        return ast.unparse(transformed_tree)

    @staticmethod
    def assert_transformed_code_equals(code, expected_result):
        transformed_code = TestObservableNamedTupleWrapper.transform_and_get_code(code)
        assert transformed_code.strip() == expected_result.strip()

    def test_simple_namedtuple(self):
        code = """
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])
p = Point(1, 2)
        """
        expected_result = """
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])
p = Point(1, 2)
p_wrapper = ObservableNamedTuple(*p)
        """
        self.assert_transformed_code_equals(code, expected_result)

    def test_nested_namedtuple(self):
        code = """
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])
Circle = namedtuple('Circle', ['center', 'radius'])
c = Circle(Point(0, 0), 5)
        """
        expected_result = """
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])
Circle = namedtuple('Circle', ['center', 'radius'])
c = Circle(Point(0, 0), 5)
c_wrapper = ObservableNamedTuple(*c)
        """
        self.assert_transformed_code_equals(code, expected_result)


def test_wrap_numpy_array():
    code = """
import numpy as np
arr = np.array([1, 2, 3])
    """
    expected_result = """
import numpy as np
arr = np.array([1, 2, 3])
arr_numpy_wrapper = ObservableNumpyArray(arr)
    """
    transformed_code = transform_code_numpy_array(code)
    assert transformed_code.strip() == expected_result.strip()


def test_wrap_nested_numpy_array():
    code = """
from numpy import array as arr
nested_arr = arr([arr([1, 2]), arr([3, 4])])
    """
    expected_result = """
from numpy import array as arr
nested_arr = arr([arr([1, 2]), arr([3, 4])])
nested_arr_numpy_wrapper = ObservableNumpyArray(nested_arr)
    """
    transformed_code = transform_code_numpy_array(code)
    assert transformed_code.strip() == expected_result.strip()


def transform_code_numpy_array(code):
    tree = ast.parse(code)
    transformer = ObservableNumpyArrayWrapper(tree)
    transformed_tree = transformer.visit(tree)
    transformed_code = ast.unparse(transformed_tree)
    return transformed_code


def test_wrap_pandas_dataframe():
    code = """
import pandas as pd
df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    """
    expected_result = """
import pandas as pd
df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
df_pandas_wrapper = ObservablePandasDataFrame(df)
    """
    transformed_code = transform_code_pandas_data_frame(code)
    assert transformed_code.strip() == expected_result.strip()


def test_wrap_nested_pandas_dataframe():
    code = """
from pandas import DataFrame as df
nested_df = df({'A': df([1, 2]), 'B': df([3, 4])})
    """
    expected_result = """
from pandas import DataFrame as df
nested_df = df({'A': df([1, 2]), 'B': df([3, 4])})
nested_df_pandas_wrapper = ObservablePandasDataFrame(nested_df)
    """
    transformed_code = transform_code_pandas_data_frame(code)
    assert transformed_code.strip() == expected_result.strip()


def transform_code_pandas_data_frame(code):
    tree = ast.parse(code)
    transformer = ObservablePandasDataFrameWrapper(tree)
    transformed_tree = transformer.visit(tree)
    transformed_code = ast.unparse(transformed_tree)
    return transformed_code
