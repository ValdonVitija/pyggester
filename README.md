# pyggester

pyggester - (python + suggester) is a static analyzer that can be used to suggest improvements to existing/functional pythonic code. 

### Prerequisites
1. Python 3.X - Preferred 3.10+
2. Install the venv module to construct a virtual env as shown in the next section

### Installation


1. Clone the repository
2. Change into the `pyggester` directory:
3. Create a virtual environment:

```
/> python3 -m venv venv
```    
4. Activate the virtual environment (*Note: the following command is for Linux systems*):

```
/> source venv/bin/activate
```
5. Install the package locally:

```
Note: This will take care of the needed dependencies and make it reachable
from every possible directory in the system, as long as your virtual environment is still activated.
** For now, you cannot pip install this package. It will be pip installable if good feedback is received. **

/> python3 setup.py install 

```
6. Move into the directory where your Python file is, and run the following command (*Note: Currently, only one argument is supported*):
 
```
*Note: Currently only one argument is supported*
/> pyggest -f python_file.py
```

### Expectations

* Do not expect this to be fully usable... not even close. This is just a glimpse of this static analyzer. Without a doubt, I expect it to be buggy.
