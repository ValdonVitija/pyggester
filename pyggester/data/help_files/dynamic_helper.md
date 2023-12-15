# Usage (Step-by-Step)

## Single File Usage


Lets suppose you have a single python file that you want to dynamically analyze(run-time analysis)

### 1. Preparation

Before code transformation with pyggester:
```bash
(venv) root@user:~/my_app> ls
app.py
```

Content of app.py:

```python
def sum_of_integers(integer_list):
    total = sum(integer_list)
    return total

my_list = [1, 2, 3, 4, 5]
print(sum_of_integers(my_list))

```
### 2. Transformation

> [!IMPORTANT]
> **Make sure you're in a virtual environment with pyggester installed before going to the next step.**

```bash
(venv) root@devs04:~/my_app> pyggest transform app.py
╭──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ File transformed successfully!                                                                                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
### 3. Post-Transformation

```bash
(venv) root@devs04:~/my_app> ls
app.py  app_transformed.py
```

Content of app_transformed.py:

```python
from pyggester.observable_collector import OBSERVABLE_COLLECTOR
from pyggester.observables import ObservableNumpyArray, ObservableNamedTuple, ObservableSet, ObservablePandasDataFrame, ObservableList, ObservableDict, ObservableTuple


def sum_of_integers(integer_list):
    total = sum(integer_list)
    return total


my_list = ObservableList([1, 2, 3, 4, 5])
OBSERVABLE_COLLECTOR.append(my_list)
print(sum_of_integers(my_list))

for observable in OBSERVABLE_COLLECTOR:
    observable.run()

```

> [!IMPORTANT]
> We now have a new file, automatically created, that mirrors the original file. This new file includes all the contents of the original, plus extra code for analyzing your code during runtime. Instead of running the original 'app.py', you should now run 'app_transformed.py'. Rest assured, everything from 'app.py' is retained in 'app_transformed.py'.

### 4. Running the Transformed Code

```bash
(venv) root@devs04:~/my_app> python3 app_transformed.py
15
╭────────────────────────────────────────────────────────────────────────────╮
│ 10 | Suggestions(/root/my_app/app_transformed.py):                         │
│     [*] Consider using an array.array instead of a list, for optimal       │
│ memory consumption                                                         │
│     [*] Consider using a set instead of a list, because of unique elements │
╰────────────────────────────────────────────────────────────────────────────╯
```

## Directory Usage

Lets suppose you have a python project(directory/repo) that you want to dynamically analyze(run-time analysis)

### 1. Preparation

Before code transformation with pyggester:
```bash
(venv) root@devs04:~/python_demo/app_dir> ls
__pycache__  app.py  temperature.py  weather.py
```

Content of app.py:

```python
import weather
import temperature


def main():
    city = input('Enter a city name: ')
    weather_condition = weather.get_weather(city)
    avg_temp = temperature.get_average_temperature()
    print(f'Weather in {city}: {weather_condition}')
    print(f'Average temperature: {avg_temp} degrees Celsius')


main()
```

Content of temperature.py:
```python
temperatures = list([20, 22, 15, 18, 20, 21, 22, 22, 18, 17, 20])


def get_average_temperature():
    return sum(temperatures) / len(temperatures)

```

Content of weather.py:
```python
weather_conditions = ['Sunny', 'Rainy', 'Cloudy', 'Windy', 'Sunny', 'Cloudy']

def get_weather(city):
    return weather_conditions.pop()
```

### 2. Transformation

> [!IMPORTANT]
> **Make sure you're in a virtual environment with pyggester installed before going to the next step.**

```bash
(venv) root@devs04:~/python_demo> pyggest transform app_dir/
Enter the name of the main file: app.py
╭──────────────────────────────────────────────────────────────────────────╮
│ Directory transformed successfully!                                      │
╰──────────────────────────────────────────────────────────────────────────╯
```
> [!IMPORTANT]
> When a directory or project is specified as an argument, pyggester prompts us to specify the main file of our project. This file should be the entry point of your project, indicated by its file name.

### 3. Post-Transformation

```bash
(venv) root@devs04:~/python_demo> ls
app_dir  app_dir_transformed
```

Content of app_dir_transformed/:

```python
(venv) root@devs04:~/python_demo/app_dir_transformed> ls
app.py  temperature.py  weather.py
```

Content of app.py:
```python
from pyggester.observable_collector import OBSERVABLE_COLLECTOR
from pyggester.observables import ObservableNumpyArray, ObservableList, ObservablePandasDataFrame, ObservableNamedTuple, ObservableSet, ObservableDict, ObservableTuple
import weather
import temperature


def main():
    city = input('Enter a city name: ')
    weather_condition = weather.get_weather(city)
    avg_temp = temperature.get_average_temperature()
    print(f'Weather in {city}: {weather_condition}')
    print(f'Average temperature: {avg_temp} degrees Celsius')


main()
for observable in OBSERVABLE_COLLECTOR:
    observable.run()

```

Content of temperature.py:
```python
from pyggester.observable_collector import OBSERVABLE_COLLECTOR
from pyggester.observables import ObservableNumpyArray, ObservableList, ObservablePandasDataFrame, ObservableNamedTuple, ObservableSet, ObservableDict, ObservableTuple
temperatures = ObservableList(list([20, 22, 15, 18, 20, 21, 22, 22, 18, 17,
    20]))
OBSERVABLE_COLLECTOR.append(temperatures)


def get_average_temperature():
    return sum(temperatures) / len(temperatures)

```

Content of weather.py:

```python
from pyggester.observable_collector import OBSERVABLE_COLLECTOR
from pyggester.observables import ObservableNumpyArray, ObservableList, ObservablePandasDataFrame, ObservableNamedTuple, ObservableSet, ObservableDict, ObservableTuple
weather_conditions = ObservableList(['Sunny', 'Rainy', 'Cloudy', 'Windy',
    'Sunny', 'Cloudy'])
OBSERVABLE_COLLECTOR.append(weather_conditions)


def get_weather(city):
    return weather_conditions.pop()

```

> [!IMPORTANT]
> We now have a new directory, automatically created, that mirrors the original directory. This new directory includes all the contents of the original, plus extra code for analyzing your code during runtime. Instead of running the original 'app.py', you should now run 'app.py' that resides inside 'app_dir_transformed/'. Rest assured, everything from 'app_dir' is retained in 'app_dir_transformed/'.

### 4. Running the Transformed Code

```bash
(venv) root@devs04:~/python_demo/app_dir_transformed> python3 app.py
Enter a city name: Pristina
Weather in Pristina: Cloudy
Average temperature: 19.545454545454547 degrees Celsius
╭─────────────────────────────────────────────────────────────────────────────────────╮
│ 3 | Suggestions(/root/python_demo/app_dir_transformed/temperature.py):              │
│     [*] Consider using an array.array instead of a list, for optimal memory         │
│ consumption                                                                         │
╰─────────────────────────────────────────────────────────────────────────────────────╯
```