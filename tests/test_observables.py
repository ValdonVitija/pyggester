from collections import namedtuple
import numpy
import pandas as pd
from pyggester.observables import (
    ObservableList,
    ObservableDict,
    ObservableNamedTuple,
    ObservableNumpyArray,
    ObservablePandasDataFrame,
    ObservableSet,
    ObservableTuple,
)


def test_different_ways_of_list_initialization():
    assert isinstance(ObservableList([1, 2, 3]), list)
    assert isinstance(ObservableList(list([1, 2, 3])), list)


def test_original_list_behavior():
    obs_list = ObservableList([1, 2, 3])
    regular_list = [1, 2, 3]

    assert obs_list == regular_list
    assert len(obs_list) == len(regular_list)
    assert obs_list[1] == regular_list[1]
    assert obs_list[1:3] == regular_list[1:3]
    assert list(obs_list) == regular_list
    assert 2 in obs_list
    assert 4 not in obs_list
    assert obs_list.copy() == regular_list.copy()
    obs_list.clear()
    regular_list.clear()
    assert len(obs_list) == 0
    assert len(regular_list) == 0
    obs_list.extend([4, 5, 6])
    regular_list.extend([4, 5, 6])
    assert obs_list == regular_list
    assert obs_list.pop() == regular_list.pop()
    assert obs_list == regular_list
    obs_list.remove(4)
    regular_list.remove(4)
    assert obs_list == regular_list
    obs_list.reverse()
    regular_list.reverse()
    assert obs_list == regular_list
    obs_list.sort()
    regular_list.sort()
    assert obs_list == regular_list


def check_observable_list_additional_attributes_test():
    obs_list = ObservableList([1, 2, 3])
    assert hasattr(obs_list, "appended")
    assert hasattr(obs_list, "extended")
    assert hasattr(obs_list, "inserted")
    assert hasattr(obs_list, "removed")
    assert hasattr(obs_list, "count_")
    assert hasattr(obs_list, "in_operator_used")
    assert hasattr(obs_list, "message_handler")


def test_check_numpy_array_instead_of_list():
    obs_list = ObservableList([[1, 2], [3, 4]])
    obs_list.check_numpy_array_instead_of_list()

    assert (
        "Consider using a numpy array instead of a list, for faster computations and optimized memory utilization"
        in obs_list.message_handler.messages
    )

    obs_list = ObservableList([1, 2, 3])
    obs_list.check_numpy_array_instead_of_list()
    assert (
        "Consider using a numpy array instead of a list, for faster computations and optimized memory utilization"
        not in obs_list.message_handler.messages
    )


def test_check_array_instead_of_list():
    obs_list = ObservableList([1, 2, 3])
    obs_list.check_array_instead_of_list()
    assert (
        "Consider using an array.array instead of a list, for optimal memory consumption"
        in obs_list.message_handler.messages
    )

    obs_list = ObservableList(["a", "b", "c"])
    obs_list.check_array_instead_of_list()
    assert (
        "Consider using an array.array instead of a list, for optimal memory consumption"
        in obs_list.message_handler.messages
    )


def test_check_list_to_set_conversion():
    obs_list = ObservableList([1, 2, 2, 3])
    result = obs_list.check_list_to_set_conversion()
    assert not result

    obs_list = ObservableList([1, 2, 3])
    result = obs_list.check_list_to_set_conversion()
    assert result


def test_check_set_instead_of_list():
    obs_list = ObservableList([1, 2, 3])
    obs_list.in_operator_used = True
    obs_list.check_set_instead_of_list()
    assert (
        "Consider using a set instead of a list, because of unique elements and element existence checking"
        in obs_list.message_handler.messages
    )

    obs_list = ObservableList([1, 2, 3])
    obs_list.in_operator_used = False
    obs_list.check_set_instead_of_list()
    assert (
        "Consider using a set instead of a list, because of unique elements"
        in obs_list.message_handler.messages
    )


def test_check_Counter_insteaf_of_list():
    obs_list = ObservableList([1, 2, 2, 3])
    obs_list.count_ = True
    obs_list.check_Counter_insteaf_of_list()
    assert (
        "Consider using a collections.Counter, to count occurences of elements"
        in obs_list.message_handler.messages
    )

    obs_list = ObservableList([1, 2, 3])
    obs_list.count_ = False
    obs_list.check_Counter_insteaf_of_list()
    assert (
        "Consider using a collections.Counter, to count occurences of elements"
        not in obs_list.message_handler.messages
    )


def test_check_tuple_instead_of_list():
    obs_list = ObservableList(["A", "B", "C"])
    obs_list.appended = False
    obs_list.extended = False
    obs_list.removed = False
    obs_list.inserted = False
    obs_list.check_tuple_instead_of_list()
    assert (
        "Consider using a tuple since all elements seem to be constants, because the list was never modified"
        in obs_list.message_handler.messages
    )

    obs_list = ObservableList(["a", "b", "c"])
    obs_list.appended = True
    obs_list.extended = True
    obs_list.removed = True
    obs_list.inserted = True
    obs_list.check_tuple_instead_of_list()
    assert (
        "Consider using a tuple since all elements seem to be constants, because the list was never modified"
        not in obs_list.message_handler.messages
    )


def test_different_ways_of_set_initialization():
    assert isinstance(ObservableSet({1, 2, 3}), set)
    assert isinstance(ObservableSet(set({1, 2, 3})), set)


def test_original_set_behavior():
    obs_set = ObservableSet({1, 2, 3})
    regular_set = {1, 2, 3}
    assert obs_set == regular_set
    assert len(obs_set) == len(regular_set)
    assert set(obs_set) == regular_set
    assert 2 in obs_set
    assert 4 not in obs_set
    obs_set.add(4)
    regular_set.add(4)
    assert obs_set == regular_set
    obs_set.discard(3)
    regular_set.discard(3)
    assert obs_set == regular_set
    obs_set.clear()
    regular_set.clear()
    assert len(obs_set) == 0
    assert len(regular_set) == 0
    obs_set.update({4, 5, 6})
    regular_set.update({4, 5, 6})
    assert obs_set == regular_set
    obs_set.remove(4)
    regular_set.remove(4)
    assert obs_set == regular_set
    popped_obs = obs_set.pop()
    popped_regular = regular_set.pop()
    assert popped_obs == popped_regular
    diff_obs = obs_set.difference({5, 6})
    diff_regular = regular_set.difference({5, 6})
    assert diff_obs == diff_regular
    union_obs = obs_set.union({6, 7})
    union_regular = regular_set.union({6, 7})
    assert union_obs == union_regular
    intersection_obs = obs_set.intersection({5, 6, 7})
    intersection_regular = regular_set.intersection({5, 6, 7})
    assert intersection_obs == intersection_regular
    sym_diff_obs = obs_set.symmetric_difference({6, 7, 8})
    sym_diff_regular = regular_set.symmetric_difference({6, 7, 8})
    assert sym_diff_obs == sym_diff_regular


def check_observable_set_additional_attributes_test():
    obs_set = ObservableSet({1, 2, 3})
    assert hasattr(obs_set, "poped")
    assert hasattr(obs_set, "removed")
    assert hasattr(obs_set, "added")
    assert hasattr(obs_set, "updated")
    assert hasattr(obs_set, "if_it_was_a_list")
    assert hasattr(obs_set, "message_handler")


def test_check_frozenset_instead_of_set():
    obs_set = ObservableSet({1, 2, 3})
    obs_set.check_frozenset_instead_of_set()
    assert (
        "Consider using a frozenset, because no modification operation has been used on set."
        in obs_set.message_handler.messages
    )


def test_check_list_instead_of_set():
    obs_set = ObservableSet({})
    obs_set.add(1)
    obs_set.add(1)
    obs_set.add(1)
    obs_set.check_list_instead_of_set()
    assert (
        "If you inteded to keep duplicates use a list instead, because we noticed a lot of duplicates entered the set"
        in obs_set.message_handler.messages
    )


def test_different_ways_of_tuple_initialization():
    assert isinstance(ObservableTuple((1, 2, 3)), tuple)
    assert isinstance(ObservableTuple(tuple([1, 2, 3])), tuple)


def test_original_tuple_behavior():
    obs_tuple = ObservableTuple((1, 2, 3))
    regular_tuple = (1, 2, 3)
    assert obs_tuple == regular_tuple
    assert len(obs_tuple) == len(regular_tuple)
    assert obs_tuple[1] == regular_tuple[1]
    assert obs_tuple[1:3] == regular_tuple[1:3]
    assert tuple(obs_tuple) == regular_tuple
    assert 2 in obs_tuple
    assert 4 not in obs_tuple
    concat_obs = obs_tuple + (4, 5)
    concat_regular = regular_tuple + (4, 5)
    assert concat_obs == concat_regular
    repeat_obs = obs_tuple * 2
    repeat_regular = regular_tuple * 2
    assert repeat_obs == repeat_regular


def check_observable_tuple_additional_attributes_test():
    obs_tuple = ObservableTuple((1, 2, 3))
    assert hasattr(obs_tuple, "mul_")
    assert hasattr(obs_tuple, "message_handler")


def test_check_mutable_inside_tuple():
    obs_tuple = ObservableTuple((1, [2, 3], 4))
    obs_tuple.check_mutable_inside_tuple()
    assert (
        "Mutable element inside of a tuple. Consider using only immutables for optimal performance"
        in obs_tuple.message_handler.messages
    )


def test_check_set_instead_of_tuple():
    obs_tuple = ObservableTuple((1, 2, 3))
    obs_tuple.check_set_instead_of_tuple()
    assert (
        "Consider using a set since elements are all unique"
        in obs_tuple.message_handler.messages
    )


def test_check_tuple_multiplication():
    obs_tuple = ObservableTuple((1, 2, 3))
    _ = obs_tuple * 2
    obs_tuple.check_tuple_multiplication()
    assert (
        "You multipled the tuple with a scalar value. If you inteded to multiply each element by that value, use a numpy array instead of a tuple."
        in obs_tuple.message_handler.messages
    )


def test_different_ways_of_dict_initialization():
    assert isinstance(ObservableDict({"a": 1, "b": 2, "c": 3}), dict)
    assert isinstance(ObservableDict(dict({"a": 1, "b": 2, "c": 3})), dict)


def test_original_dict_behavior():
    obs_dict = ObservableDict({"a": 1, "b": 2, "c": 3})
    regular_dict = {"a": 1, "b": 2, "c": 3}
    assert obs_dict == regular_dict
    assert len(obs_dict) == len(regular_dict)
    assert obs_dict["a"] == regular_dict["a"]
    obs_dict["d"] = 4
    assert obs_dict == {"a": 1, "b": 2, "c": 3, "d": 4}
    del obs_dict["a"]
    assert obs_dict == {"b": 2, "c": 3, "d": 4}
    regular_dict["d"] = 4
    assert regular_dict == {"a": 1, "b": 2, "c": 3, "d": 4}
    del regular_dict["a"]
    assert regular_dict == {"b": 2, "c": 3, "d": 4}
    popped_item_obs = obs_dict.popitem()
    popped_item_reg = regular_dict.popitem()
    assert popped_item_obs == popped_item_reg
    popped_obs = obs_dict.pop("b")
    popped_reg = regular_dict.pop("b")
    assert popped_obs == popped_reg
    obs_dict.update({"e": 5})
    print(obs_dict)
    assert obs_dict == {"c": 3, "e": 5}
    regular_dict.update({"e": 5})
    assert regular_dict == {"c": 3, "e": 5}
    copy_obs = obs_dict.copy()
    assert copy_obs == obs_dict
    assert set(obs_dict.keys()) == set(regular_dict.keys())
    assert set(obs_dict.values()) == set(regular_dict.values())
    assert set(obs_dict.items()) == set(regular_dict.items())


def check_observable_dict_additional_attributes_test():
    obs_dict = ObservableDict({"a": 1, "b": 2, "c": 3})
    assert hasattr(obs_dict, "keys_")
    assert hasattr(obs_dict, "update_")
    assert hasattr(obs_dict, "setitem_")
    assert hasattr(obs_dict, "delitem_")
    assert hasattr(obs_dict, "getitem_")
    assert hasattr(obs_dict, "pop_")
    assert hasattr(obs_dict, "items_")
    assert hasattr(obs_dict, "clear_")
    assert hasattr(obs_dict, "values_")
    assert hasattr(obs_dict, "message_handler")


def test_check_Counter_instead_of_dict():
    obs_dict = ObservableDict(a=1, b=2, c=3)
    obs_dict.check_Counter_instead_of_dict()
    assert (
        "If you are using this dict to store occurences of elements, consider using a collections.Counter"
        in obs_dict.message_handler.messages
    )


def test_check_dict_get_method():
    obs_dict = ObservableDict(a=1, b=2, c=3)
    _ = obs_dict["a"]
    obs_dict.check_dict_get_method()
    assert (
        "For dict key retreval, always consider using 'your_dict'.get('key') instead of 'your_dict'['key']"
        in obs_dict.message_handler.messages
    )


def test_check_list_instead_of_dict():
    obs_dict = ObservableDict(a=1, b=2, c=3)
    _ = obs_dict.values()
    obs_dict.check_list_instead_of_dict()
    assert (
        "It seems like you never used this dict for anything otherthan somehow using the values, use a list/array"
        in obs_dict.message_handler.messages
    )


def test_check_array_data_type():
    arr = numpy.array([1, 2, 3], dtype=numpy.int64)
    obs_array = ObservableNumpyArray(arr)
    obs_array.check_array_data_type()
    assert (
        "Array was initiated with int64 integers, but values do not exceed 3. Consider using uint8 for optimization."
        in obs_array.message_handler.messages
    )


def test_check_array_sparsity():
    arr = numpy.array([0, 0, 1, 0, 0, 0, 0, 0, 0, 0])
    obs_array = ObservableNumpyArray(arr)
    obs_array.check_array_sparsity()
    assert (
        "The array is highly sparse (sparsity: 90.00%). Consider using a sparse array representation for memory efficiency."
        in obs_array.message_handler.messages
    )


def test_check_for_nan_values():
    arr = numpy.array([1, numpy.nan, 3])
    obs_array = ObservableNumpyArray(arr)
    obs_array.check_for_nan_values()
    assert (
        "The array contains NaN values. Consider using masked arrays or handling NaN values appropriately."
        in obs_array.message_handler.messages
    )


def test_check_for_monotonicity():
    arr = numpy.array([1, 2, 3, 4, 5])
    obs_array = ObservableNumpyArray(arr)
    obs_array.check_for_monotonicity()
    assert (
        "The array is monotonic. Consider using specialized algorithms or data structures for monotonic arrays."
        in obs_array.message_handler.messages
    )


def test_check_for_categorical_data():
    arr = numpy.array(
        ["dog", "cat", "dog", "bird", "dog", "cat", "bird", "bird", "cat"]
    )

    obs_array = ObservableNumpyArray(arr)
    obs_array.check_for_categorical_data()
    assert (
        "The array contains categorical data with 3 unique values. Consider using categorical data types for efficiency, like pd.Categorical()"
        in obs_array.message_handler.messages
    )


def test_check_for_symmetry():
    arr = numpy.array([[1, 2], [2, 1]])
    obs_array = ObservableNumpyArray(arr)
    obs_array.check_for_symmetry()
    assert (
        "The array is symmetric. Consider using specialized algorithms to operate on symmetric arrays, for example functions from scipy"
        in obs_array.message_handler.messages
    )


def test_check_for_constant_values():
    arr = numpy.array([1, 1, 1, 1])
    obs_array = ObservableNumpyArray(arr)
    obs_array.check_for_constant_values()
    assert (
        "All elements in the array are the same. Consider using a single value, a constant or collections.Counter for memory efficiency."
        in obs_array.message_handler.messages
    )


def test_check_for_missing_values():
    df = pd.DataFrame({"A": [1, 2, None], "B": [4, 5, 6]})
    observable_df = ObservablePandasDataFrame(df)
    observable_df.check_for_missing_values()
    assert (
        "The DataFrame contains missing values. Consider handling missing values."
        in observable_df.message_handler.messages
    )


def test_check_for_constant_columns():
    df = pd.DataFrame({"A": [1, 1, 1], "B": [4, 5, 6]})
    observable_df = ObservablePandasDataFrame(df)
    observable_df.check_for_constant_columns()
    assert (
        "The DataFrame contains constant columns (['A']). Consider dropping them for memory efficiency."
        in observable_df.message_handler.messages
    )


def test_check_for_duplicate_rows():
    df = pd.DataFrame({"A": [1, 2, 2], "B": [4, 5, 5]})
    observable_df = ObservablePandasDataFrame(df)
    observable_df.check_for_duplicate_rows()
    assert (
        "The DataFrame contains duplicate rows. Consider handling duplicate rows appropriately."
        in observable_df.message_handler.messages
    )


def test_check_series_instead_of_dataframe():
    df = pd.DataFrame({"A": [1, 2, 3]})
    observable_df = ObservablePandasDataFrame(df)
    observable_df.check_series_insteafd_of_dataframe()
    assert (
        "Consider using a Series instead of a DataFrame when you have only one column of data."
        in observable_df.message_handler.messages
    )


def test_check_numpy_instead_of_dataframe():
    df = pd.DataFrame({"A": range(15000), "B": range(15000)})
    observable_df = ObservablePandasDataFrame(df)
    observable_df.check_numpy_instead_of_dataframe()
    assert (
        "Consider using a NumPy array or a specialized data structure if you have a large number of rows and a small number of columns."
        in observable_df.message_handler.messages
    )


def test_check_for_excessive_nesting():
    InnerTuple = namedtuple("InnerTuple", "field1 field2")
    OuterTuple = namedtuple("OuterTuple", "inner")
    outer_instance = OuterTuple(InnerTuple(1, 2))
    observable_tuple = ObservableNamedTuple(outer_instance)
    observable_tuple.check_for_excessive_nesting()
    assert (
        "Avoid excessive nesting of namedtuples to keep the structure simple and readable. Consider usina a class instead"
        in observable_tuple.message_handler.messages
    )


def test_check_for_ignoring_type_annotations():
    MyTuple = namedtuple("MyTuple", "field1 field2")
    my_tuple_instance = MyTuple(1, 2)
    observable_tuple = ObservableNamedTuple(my_tuple_instance)
    observable_tuple.check_for_ignoring_type_annotations()
    assert (
        "Consider using type annotations for field in namedtuples for better documentation."
        in observable_tuple.message_handler.messages
    )


def test_check_for_ignoring_namedtuple_advantages():
    ManyFields = namedtuple("ManyFields", " ".join(f"field{i}" for i in range(11)))
    many_fields_instance = ManyFields(*(range(11)))
    observable_tuple = ObservableNamedTuple(many_fields_instance)
    observable_tuple.check_for_ignoring_namedtuple_advantages()
    assert (
        "Consider using namedtuples for simpler data structures with fewer fields for better readability."
        in observable_tuple.message_handler.messages
    )
