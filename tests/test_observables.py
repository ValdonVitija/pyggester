import array
from collections import Counter
import numpy as np
import pytest
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
        "Consider using a set instead of a list, because of unique elements and elemnt existence checking"
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
