from typing import List, Tuple, Dict, Any
from collections import namedtuple
import numpy
from message_handler import MessageHandler
import array
import inspect
import pathlib
from typing import List, Dict, Any, Tuple

OBSERVABLE_RUNNER = []


class ObservableList(list):
    __slots__: Tuple[str] = (
        "appended",
        "extended",
        "inserted",
        "removed",
        "in_operator_used",
        "message_handler",
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.appended: bool = False
        self.extended: bool = False
        self.inserted: bool = False
        self.removed: bool = False
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
        """ """
        if all(isinstance(item, int) for item in self):
            if array.array("i", self):
                return True
        elif all(isinstance(item, float) for item in self):
            if array.array("d", self):
                return True
        elif all(isinstance(item, str) and len(item) == 1 for item in self):
            if array.array("c", self):
                return True
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

    def run(self):
        """
        Only run checkers so that we offer a better running interface
        for each observable.

        Added checkers should be called here in sequence
        Might need to refactor this to add priority levels and maybe
        only give a single suggestions, but that needs way more specific analysis
        """
        self.check_array_instead_of_list()
        self.check_numpy_array_instead_of_list()
        self.check_set_instead_of_list()
        self.message_handler.print_messages()


class ObservableSet(set):
    __slots__: Tuple[set] = ()

    def __init__(self) -> None:
        pass


class ObservableTuple(tuple):
    __slots__: Tuple[set] = ()

    def __init__(self) -> None:
        pass


class ObservableDict(dict):
    __slots__: Tuple[set] = ()

    def __init__(self) -> None:
        pass


class ObservableNamedTuple:
    __slots__: Tuple[set] = ("namedtuple__",)

    def __init__(self, namedtuple__) -> None:
        self.namedtuple__ = namedtuple__


# Car = namedtuple("Car", ObservableList(["brand", "model"]))
# car_1 = Car(brand="tesla", model="x")
# car_1_wrapper = ObservableNamedTuple(car_1)
# print(dir(car_1_wrapper))

my_list = ObservableList([1, 4, 3])
OBSERVABLE_RUNNER.append(my_list)
for observable in OBSERVABLE_RUNNER:
    observable.run()
