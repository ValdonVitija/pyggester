from _collections_abc import dict_items, dict_keys, dict_values
from typing import List, Tuple, Dict, Any, Iterable
from collections import namedtuple
import numpy
from pyggester.message_handler import MessageHandler
import array
import scipy.sparse as sp
import inspect
from typing import List, Dict, Any, Tuple, Set, NamedTuple

# TODO MIGHT CONSIDER CREATING AN OBSERVABLE ABSTRACT BASE CLASS,
# TO MAKE EACH OBSERVABLE FOLLOW A SPECIFIC CONTRACT


class ObservableList(list):
    """
    The ObservableList is an enhanced version of a list that
    preserves the full original functionality of a list, but
    adds more features to it so that we keep track of anything that
    potentially happens in order to do dynamic analysis to each declared
    list.
    """

    __slots__: Tuple[str] = (
        "appended",
        "extended",
        "inserted",
        "removed",
        "count_",
        "in_operator_used",
        "message_handler",
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # The following methods keep track of base list methods.
        # False if not used(ever), True if used
        self.appended: bool = False
        self.extended: bool = False
        self.inserted: bool = False
        self.removed: bool = False
        self.count_: bool = False
        self.in_operator_used: bool = False
        """
        Get the context of the current list being analyzed
        """
        caller_frame = inspect.currentframe().f_back
        line_number: int = caller_frame.f_lineno
        file_path: str = caller_frame.f_globals["__file__"]

        self.message_handler = MessageHandler(line_nr=line_number, file_path=file_path)

    def append(self, item) -> None:
        super().append(item)
        self.appended = True

    def extend(self, iterable) -> None:
        super().extend(iterable)
        self.extended = True

    def insert(self, index, item) -> None:
        super().insert(index, item)
        self.inserted = True

    def remove(self, item) -> None:
        super().remove(item)
        self.removed = True

    def count(self, __value: Any) -> int:
        self.count_ = True
        return super().count(__value)

    def __contains__(self, __key: object) -> bool:
        self.in_operator_used = True
        return super().__contains__(__key)

    def get_list_dimension(self, lst):
        """ """
        if not isinstance(lst, list):
            return 0
        else:
            inner_dimensions = [self.get_list_dimension(item) for item in lst]
            return 1 + max(inner_dimensions, default=0)

    def check_numpy_array_instead_of_list(self):
        """ """
        try:
            if self.get_list_dimension(self) >= 2:
                numpy.array(self)
                self.message_handler.messages.append(
                    "Consider using a numpy array instead of a list, for faster computations and optimized memory utilization"
                )
        except Exception:
            pass

    def check_array_instead_of_list(self):
        if self.can_list_be_converted_to_array():
            self.message_handler.messages.append(
                "Consider using an array.array instead of a list, for optimal memory consumption"
            )

    def can_list_be_converted_to_array(self):
        """
        Check if the list can be converted to an array.

        Returns:
            bool: True if the list can be converted, False otherwise.
        """
        if all(isinstance(item, int) for item in self):
            return True
        elif all(isinstance(item, float) for item in self):
            return True
        elif all(isinstance(item, str) and len(item) == 1 for item in self):
            try:
                array.array("u", self)
                return True
            except ValueError:
                return False
        else:
            return False

    def check_list_to_set_conversion(self):
        if len(self) == len(set(self)):
            return True
        return False

    def check_set_instead_of_list(self):
        if self.check_list_to_set_conversion():
            if self.in_operator_used:
                self.message_handler.messages.append(
                    "Consider using a set instead of a list, because of unique elements and elemnt existence checking"
                )
            else:
                self.message_handler.messages.append(
                    "Consider using a set instead of a list, because of unique elements"
                )

    def check_Counter_insteaf_of_list(self):
        if self.count_:
            self.message_handler.messages.append(
                "Consider using a collections.Counter, to count occurences of elements"
            )

    def check_tuple_instead_of_list(self):
        all__ = []
        for x in self:
            if isinstance(x, str):
                if x.isupper() or x[0].isupper():
                    all__.append(True)

        if len(all__) == len(self) and not any(
            [self.appended, self.extended, self.removed, self.inserted]
        ):
            self.message_handler.messages.append(
                "Consider using a tuple since all elements seem to be constants, because the list was never modified"
            )

    def run(self):
        """
        Only run checkers so that we offer a better running interface
        for each observable.

        Added checkers should be called here in sequence
        Might need to refactor this to add priority levels and maybe
        only give a single suggestion, but that needs way more specific analysis
        """
        self.check_array_instead_of_list()
        self.check_numpy_array_instead_of_list()
        self.check_set_instead_of_list()
        self.check_Counter_insteaf_of_list()
        self.message_handler.print_messages()


class ObservableSet(set):
    """
    The ObservableSet is an enhanced version of a set that
    preserves the full original functionality of a set, but
    adds more features to it so that we keep track of anything that
    potentially happens in order to do dynamic analysis to each declared
    set.
    """

    __slots__: Tuple[set] = (
        "poped",
        "removed",
        "added",
        "updated",
        "message_handler",
        "if_it_was_a_list",
    )

    def __init__(self, iterable=None) -> None:
        super().__init__(iterable)
        self.poped: bool = False
        self.removed: bool = False
        self.added: bool = False
        self.updated: bool = False
        self.if_it_was_a_list: List[Any] = []

        caller_frame = inspect.currentframe().f_back
        line_number: int = caller_frame.f_lineno
        file_path: str = caller_frame.f_globals["__file__"]

        self.message_handler = MessageHandler(line_nr=line_number, file_path=file_path)

    def add(self, element: Any) -> None:
        super().add(element)
        self.added = True
        self.if_it_was_a_list.append(element)

    def pop(self) -> Any:
        self.poped = True
        return super().pop()

    def remove(self, element: Any) -> None:
        super().remove(element)
        self.removed = True

    def update(self, *others: Iterable) -> None:
        super().update(*others)
        self.updated = True
        for elem_ in others:
            self.if_it_was_a_list.append(elem_)

    def check_frozenset_instead_of_set(self):
        if not any([self.added, self.removed, self.updated, self.poped]):
            self.message_handler.messages.append(
                "Consider using a frozenset, because no modification operation has been used on set."
            )

    def check_list_instead_of_set(self):
        """
        The suggestion here is quite subjective.
        NOTE: Might need to refactor this one
        """
        if len(self.if_it_was_a_list) > 1.2 * len(self) and any(
            [self.added, self.removed, self.updated, self.poped]
        ):
            self.message_handler.messages.append(
                "If you inteded to keep duplicates use a list instead, because we noticed a lot of duplicates entered the set"
            )

    def run(self):
        self.check_frozenset_instead_of_set()
        self.check_list_instead_of_set()


class ObservableTuple(tuple):
    """
    The ObservableTuple is an enhanced version of a tuple that
    preserves the full original functionality of a tuple, but
    adds more features to it so that we keep track of anything that
    potentially happens in order to do dynamic analysis to each declared
    tuple.
    """

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, *args)

    def __init__(self, *args: Any, **kwargs) -> None:
        super().__init__()
        self.mul_: bool = True

        caller_frame = inspect.currentframe().f_back
        line_number: int = caller_frame.f_lineno
        file_path: str = caller_frame.f_globals["__file__"]

        self.message_handler = MessageHandler(line_nr=line_number, file_path=file_path)

    def __mul__(self, n: int) -> "ObservableTuple":
        result = super().__mul__(n)
        return result

    def check_mutable_inside_tuple(self) -> None:
        for elem_ in self:
            if isinstance(elem_, (list, dict, set)):
                self.message_handler.messages.append(
                    "Mutable element inside of a tuple. Consider using only immutables for optimal performance"
                )

    def check_set_instead_of_tuple(self) -> None:
        try:
            if len(set(self)) == len(self):
                self.message_handler.messages.append(
                    "Consider using a set since elements are all unique"
                )
        except Exception:
            pass

    def check_tuple_multiplication(self) -> None:
        if self.mul_:
            self.message_handler.messages.append(
                "You multipled the tuple with a scalar value. If you inteded to multiply each element by that value, use a numpy array instead of a tuple."
            )

    def run(self) -> None:
        self.check_mutable_inside_tuple()
        self.check_tuple_multiplication()
        self.check_set_instead_of_tuple()


class ObservableDict(dict):
    """
    The ObservableDict is an enhanced version of a dict that
    preserves the full original functionality of a dict, but
    adds more features to it so that we keep track of anything that
    potentially happens in order to do dynamic analysis to each declared
    dict.
    """

    __slots__: Tuple[str] = (
        "keys_",
        "update_",
        "setitem_",
        "delitem_",
        "getitem_",
        "pop_",
        "items_",
        "clear_",
        "values_",
        "message_handler",
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.keys_: bool = False
        self.update_: bool = False
        self.setitem_: bool = False
        self.delitem_: bool = False
        self.getitem_: bool = False
        self.pop_: bool = False
        self.items_: bool = False
        self.clear_: bool = False
        self.values_: bool = False

        caller_frame = inspect.currentframe().f_back
        line_number: int = caller_frame.f_lineno
        file_path: str = caller_frame.f_globals["__file__"]

        self.message_handler = MessageHandler(line_nr=line_number, file_path=file_path)

    def __setitem__(self, key, value) -> None:
        super().__setitem__(key, value)
        self.setitem_ = True

    def __delitem__(self, key) -> None:
        super().__delitem__(key)
        self.delitem_ = True

    def __getitem__(self, __key: Any) -> Any:
        self.getitem_ = True
        return super().__getitem__(__key)

    def clear(self) -> None:
        super().clear()
        self.clear_ = True

    def pop(self, key, default=None) -> "ObservableDict":
        result = super().pop(key, default)
        return result

    def popitem(self) -> "ObservableDict":
        result = super().popitem()
        return result

    def update(self, *args, **kwargs) -> None:
        super().update(*args, **kwargs)
        self.update_ = True

    def setdefault(self, key, default=None) -> "ObservableDict":
        result = super().setdefault(key, default)
        return result

    def copy(self) -> "ObservableDict":
        result = super().copy()
        return result

    def keys(self) -> dict_keys:
        self.keys_ = True
        return super().keys()

    def values(self) -> dict_values:
        self.values_ = True
        return super().values()

    def items(self) -> dict_items:
        self.items_ = True
        return super().items()

    def check_Counter_instead_of_dict(self) -> None:
        if all([True for value in self.values() if isinstance(value, int)]):
            self.message_handler.messages.append(
                "If you are using this dict to store occurences of elements, consider using a collections.Counter"
            )

    def check_dict_get_method(self) -> None:
        if self.getitem_:
            self.message_handler.messages.append(
                "For dict key retreval, always consider using 'your_dict'.get('key') instead of 'your_dict'['key']"
            )

    def check_list_instead_of_dict(self) -> None:
        """
        Suggest to use a list when a dict seems to not be used optimally
        """
        if (not any([self.getitem_, self.keys_, self.items_]) and self.values_) or (
            not any([self.getitem_, self.items_, self.values_]) and self.keys_
        ):
            self.message_handler.messages.append(
                "It seems like you never used this dict for anything otherthan somehow using the values, use a list/array"
            )

    def run(self) -> None:
        self.check_Counter_instead_of_dict()
        self.check_dict_get_method()
        self.check_list_instead_of_dict()


class ObservableNumpyArray:
    """
    The ObservableNumpyArray is a numpy analyzer that takes the declared numpy array
    and does internal attribute and value checkings for potential improvement suggestions.
    """

    __slots__: Tuple[str] = ("arr__", "message_handler")

    def __init__(self, arr__) -> None:
        self.arr__ = arr__

        caller_frame = inspect.currentframe().f_back
        line_number: int = caller_frame.f_lineno
        file_path: str = caller_frame.f_globals["__file__"]

        self.message_handler = MessageHandler(line_nr=line_number, file_path=file_path)

    def check_array_data_type(self) -> None:
        """ """
        current_dtype = self.arr__.dtype
        min_dtype = numpy.min_scalar_type(numpy.max(self.arr__))
        max_number = numpy.max(self.arr__)
        if current_dtype != min_dtype:
            self.message_handler.messages.append(
                f"Array was initiated with {current_dtype} integers, but values do not exceed {max_number}. Consider using {min_dtype} for optimization."
            )

    def check_array_sparsity(self, threshold: float = 0.8) -> None:
        """Suggests using sparse arrays for highly sparse data to save memory."""

        sparsity = 1.0 - numpy.count_nonzero(self.arr__) / float(self.arr__.size)
        if sparsity > threshold:
            try:
                _ = sp.csr_matrix(self.arr__)
                self.message_handler.messages.append(
                    f"The array is highly sparse (sparsity: {sparsity:.2%}). Consider using a sparse array representation for memory efficiency."
                )
            except Exception:
                pass

    def check_for_nan_values(self) -> None:
        """Suggests using masked arrays or handling NaN values."""

        if numpy.isnan(self.arr__).any():
            try:
                _ = numpy.ma.masked_array(self.arr__, mask=numpy.isnan(self.arr__))
                self.message_handler.messages.append(
                    "The array contains NaN values. Consider using masked arrays or handling NaN values appropriately."
                )
            except Exception:
                pass

    def check_for_monotonicity(self) -> None:
        """Suggests using specialized algorithms or data structures for monotonic arrays."""

        if numpy.all(numpy.diff(self.arr__) >= 0) or numpy.all(
            numpy.diff(self.arr__) <= 0
        ):
            self.message_handler.messages.append(
                "The array is monotonic. Consider using specialized algorithms or data structures for monotonic arrays."
            )

    def check_for_categorical_data(self) -> None:
        """Suggests using categorical data types for arrays with a small number of unique values."""

        unique_values_count = len(numpy.unique(self.arr__))
        if unique_values_count < len(self.arr__) / 2:
            self.message_handler.messages.append(
                f"The array contains categorical data with {unique_values_count} unique values. Consider using categorical data types for efficiency, like pd.Categorical()"
            )

    def check_for_symmetry(self) -> None:
        """Suggests using specialized algorithms or data structures for symmetric arrays."""
        if numpy.array_equal(self.arr__, self.arr__.T):
            self.message_handler.messages.append(
                "The array is symmetric. Consider using specialized algorithms to operate on symmetric arrays, for example functions from scipy"
            )

    def check_for_constant_values(self) -> None:
        """Suggests using a single value or a constant data type if all elements are the same."""
        if numpy.all(self.arr__ == self.arr__[0]):
            self.message_handler.messages.append(
                "All elements in the array are the same. Consider using a single value, a constant or collections.Counter for memory efficiency."
            )

    def run(self) -> None:
        self.check_array_data_type()
        self.check_array_sparsity()
        self.check_for_categorical_data()
        self.check_for_constant_values()
        self.check_for_nan_values()
        self.check_for_monotonicity()
        self.check_for_symmetry()


class ObservablePandasDataFrame:
    """
    The ObservablePandasDataFrame is a Pandas DataFrame analyzer that takes the declared DataFrame
    and does internal attribute and value checkings for potential improvement suggestions.
    """

    __slots__ = ("df__", "message_handler")

    def __init__(self, df__) -> None:
        self.df__ = df__

        caller_frame = inspect.currentframe().f_back
        line_number: int = caller_frame.f_lineno
        file_path: str = caller_frame.f_globals["__file__"]

        self.message_handler = MessageHandler(line_nr=line_number, file_path=file_path)

    def check_for_missing_values(self) -> None:
        """Suggests handling missing values appropriately."""

        if self.df__.isnull().any().any():
            self.message_handler.messages.append(
                "The DataFrame contains missing values. Consider handling missing values."
            )

    def check_for_constant_columns(self) -> None:
        """Suggests dropping constant columns for memory efficiency."""

        constant_columns = self.df__.columns[self.df__.nunique() == 1]
        if constant_columns.any():
            self.message_handler.messages.append(
                f"The DataFrame contains constant columns ({constant_columns.tolist()}). Consider dropping them for memory efficiency."
            )

    def check_for_duplicate_rows(self) -> None:
        """Suggests handling duplicate rows appropriately."""

        if self.df__.duplicated().any():
            self.message_handler.messages.append(
                "The DataFrame contains duplicate rows. Consider handling duplicate rows appropriately."
            )

    def check_series_insteafd_of_dataframe(self) -> None:
        """Suggests using alternative data structures for specific scenarios."""
        if len(self.df__.columns) == 1:
            self.message_handler.messages.append(
                "Consider using a Series instead of a DataFrame when you have only one column of data."
            )

    def check_numpy_instead_of_dataframe(self) -> None:
        """"""
        if len(self.df__.index) > 10000 and len(self.df__.columns) < 5:
            self.message_handler.messages.append(
                "Consider using a NumPy array or a specialized data structure if you have a large number of rows and a small number of columns."
            )

    def run(self) -> None:
        self.check_for_constant_columns()
        self.check_for_duplicate_rows()
        self.check_for_missing_values()
        self.check_numpy_instead_of_dataframe()
        self.check_series_insteafd_of_dataframe()
        self.message_handler.print_messages()


class ObservableNamedTuple:
    """
    The ObservableNamedTuple is an enhanced version of a namedtuple that
    preserves the full original functionality of a namedtuple, but
    adds more features to it so that we keep track of anything that
    potentially happens in order to do dynamic analysis to each declared
    namedtuple.
    """

    __slots__: Tuple[set] = ("namedtuple__", "message_handler")

    def __init__(self, namedtuple__) -> None:
        self.namedtuple__ = namedtuple__

        caller_frame = inspect.currentframe().f_back
        line_number: int = caller_frame.f_lineno
        file_path: str = caller_frame.f_globals["__file__"]

        self.message_handler = MessageHandler(line_nr=line_number, file_path=file_path)

    def check_for_excessive_nesting(self) -> None:
        """Suggests avoiding excessive nesting of namedtuples."""

        for field_name in self.namedtuple__._fields:
            if isinstance(getattr(self.namedtuple__, field_name), tuple):
                self.message_handler.messages.append(
                    "Avoid excessive nesting of namedtuples to keep the structure simple and readable. Consider usina a class instead"
                )
                break

    def check_for_ignoring_type_annotations(self) -> None:
        """Suggests using type annotations to document the expected types of each field."""
        class_annotations = getattr(self.namedtuple__, "__annotations__", {})
        if not class_annotations:
            self.message_handler.messages.append(
                "Consider using type annotations for field in namedtuples for better documentation."
            )

    def check_for_ignoring_namedtuple_advantages(self) -> None:
        """Suggests taking advantage of the simplicity of namedtuples."""

        if len(self.namedtuple__._fields) > 10:
            self.message_handler.messages.append(
                "Consider using namedtuples for simpler data structures with fewer fields for better readability."
            )

    def run(self):
        self.check_for_ignoring_type_annotations()
        self.check_for_ignoring_namedtuple_advantages()
        self.check_for_excessive_nesting()
        self.message_handler.print_messages()
