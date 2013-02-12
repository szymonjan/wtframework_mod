"""
I'm overriding the 'ddt' definitions as they are causing issues with the JUnit parser by 
inserting HTML characters from the test.

@author: David Lai
"""

from functools import wraps
import re
from wtframework.wtf.data.CsvReader import CsvReader
from wtframework.wtf.data.DataManager import WTF_DATA_MANAGER

__version__ = '0.2.1wtf'

MAGIC = '%values'  # this value cannot conflict with any real python attribute


def data(*values):
    """
    Method decorator to add to your test methods.

    Should be added to methods of instances of ``unittest.TestCase``.
    """
    def wrapper(func):
        setattr(func, MAGIC, values)
        return func
    return wrapper


def csvdata(csv_file, env_prefix=None):
    """
    Method decorator to use CSV data driven tests.

    Should be added to methods of instances of ``unittest.TestCase``.
    """
    entry_list = []
    try:
        csv_file = CsvReader(WTF_DATA_MANAGER.get_data_path(csv_file, env_prefix))
        while True:
            entry_list.append(csv_file.next())
    except StopIteration:
        pass 
    values = tuple(entry_list)
    
    def wrapper(func):
        setattr(func, MAGIC, values)
        return func
    return wrapper


def ddt(cls):
    """
    Class decorator for subclasses of ``unittest.TestCase``.

    Apply this decorator to the test case class, and then
    decorate test methods with ``@data``.

    For each method decorated with ``@data``, this will effectively create as
    many methods as data items are passed as parameters to ``@data``.

    The names of the test methods follow the pattern ``test_func_name
    + "_" + str(data)``. If ``data.__name__`` exists, it is used
    instead for the test method name.
    """

    def feed_data(func, *args, **kwargs):
        """
        This internal method decorator feeds the test data item to the test.
        """
        @wraps(func)
        def wrapper(self):
            return func(self, *args, **kwargs)
        return wrapper

    for name, f in cls.__dict__.items():
        if hasattr(f, MAGIC):
            i = 0
            for v in getattr(f, MAGIC):
                test_name = getattr(v, "__name__", "{0}_{1}".format(name, v))
                #strip illegal xml characters characters. - DL
                formatted_test_name = re.sub(r'[<>&/]', '', test_name)
                setattr(cls, formatted_test_name, feed_data(f, v))
                i = i + 1
            delattr(cls, name)

    return cls

