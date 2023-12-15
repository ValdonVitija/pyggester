from pyggester.observable_collector import OBSERVABLE_COLLECTOR
from pyggester.observables import ObservableTuple, ObservablePandasDataFrame, ObservableNamedTuple, ObservableNumpyArray, ObservableSet, ObservableDict, ObservableList


def func1():
    pass


for observable in OBSERVABLE_COLLECTOR:
    observable.run()
