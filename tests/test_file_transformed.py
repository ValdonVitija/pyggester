from pyggester.observable_collector import OBSERVABLE_COLLECTOR
from pyggester.observables import ObservableList, ObservablePandasDataFrame, ObservableSet, ObservableNamedTuple, ObservableDict, ObservableNumpyArray, ObservableTuple


def func1():
    pass


for observable in OBSERVABLE_COLLECTOR:
    observable.run()
