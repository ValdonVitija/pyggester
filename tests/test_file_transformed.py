from pyggester.observable_collector import OBSERVABLE_COLLECTOR
from pyggester.observables import ObservablePandasDataFrame, ObservableList, ObservableNamedTuple, ObservableTuple, ObservableSet, ObservableDict, ObservableNumpyArray


def func1():
    pass


for observable in OBSERVABLE_COLLECTOR:
    observable.run()
