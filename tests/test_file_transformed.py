from pyggester.observable_collector import OBSERVABLE_COLLECTOR
from pyggester.observables import ObservableList, ObservableNamedTuple, ObservableSet, ObservableDict, ObservableTuple, ObservableNumpyArray, ObservablePandasDataFrame


def func1():
    pass


for observable in OBSERVABLE_COLLECTOR:
    observable.run()
