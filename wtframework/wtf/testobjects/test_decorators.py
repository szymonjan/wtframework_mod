##########################################################################
#This file is part of WTFramework. 
#
#    WTFramework is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    WTFramework is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with WTFramework.  If not, see <http://www.gnu.org/licenses/>.
##########################################################################
"""
I'm overriding the 'ddt' definitions as they are causing issues with the JUnit parser by 
inserting HTML characters from the test.

I'm also adding in a 'csvdata' method decorator for supporting csv data driven tests.

"""

from functools import wraps
from wtframework.wtf.data.data_management import CsvReader, WTF_DATA_MANAGER
import inspect
import json
import os
import re

__version__ = '0.4.0wtf'

# this value cannot conflict with any real python attribute
DATA_ATTR = '%values'

# store the path to JSON file
FILE_ATTR = '%file_path'

MAGIC = '%values'  # this value cannot conflict with any real python attribute



def data(*values):
    """
    Method decorator to add to your test methods.

    Should be added to methods of instances of ``unittest.TestCase``.
    
    Args:
        values - var args of values to run the test against.

    Usage example::

        @data('red', 'blue', orange')
        def test_color(color):
            ...

    Runs the test for each color: red, blue, orange.

    """
    def wrapper(func):
        setattr(func, MAGIC, values)
        return func
    return wrapper


def file_data(value):
    """
    Method decorator to add to your test methods.

    Should be added to methods of instances of ``unittest.TestCase``.

    ``value`` should be a path relative to the directory of the file
    containing the decorated ``unittest.TestCase``. The file
    should contain JSON encoded data, that can either be a list or a
    dict.

    In case of a list, each value in the list will correspond to one
    test case, and the value will be concatenated to the test method
    name.

    In case of a dict, keys will be used as suffixes to the name of the
    test case, and values will be fed as test data.
    """
    def wrapper(func):
        setattr(func, FILE_ATTR, value)
        return func
    return wrapper


def csvdata(csv_file, env_prefix=None):
    """
    Method decorator to use CSV data driven tests.

    Should be added to methods of instances of ``unittest.TestCase``.
    
    Args:
        csv_file (str) : name of CSV file
    
    Kwargs:
        env_prefix (str) : subfolder of /data directory to pull csv file from.

    Example::
        
        @csvdata('mydatafile.csv', env_prefix='qa')
        def test_datadriven_test(data):
            print "column1 data is:", data['column1_name']
        
        
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


    def process_file_data(name, func, file_attr):
        """
        Process the parameter in the `file_data` decorator.
        """
        cls_path = os.path.abspath(inspect.getsourcefile(cls))
        data_file_path = os.path.join(os.path.dirname(cls_path), file_attr)

        def _raise_ve(*args):
            raise ValueError("%s does not exist" % file_attr)

        if os.path.exists(data_file_path) is False:
            test_name = "{0}_{1}".format(name, "error")
            setattr(cls, test_name, feed_data(_raise_ve, None))
        else:
            data = json.loads(open(data_file_path).read())
            for elem in data:
                if isinstance(data, dict):
                    key, value = elem, data[elem]
                    test_name = "{0}_{1}".format(name, key)
                elif isinstance(data, list):
                    value = elem
                    test_name = "{0}_{1}".format(name, value)
                setattr(cls, test_name, feed_data(func, value))

    for name, func in list(cls.__dict__.items()):
        if hasattr(func, DATA_ATTR):
            for v in getattr(func, DATA_ATTR):
                test_name = getattr(v, "__name__", "{0}_{1}".format(name, v))
                setattr(cls, test_name, feed_data(func, v))
            delattr(cls, name)
        elif hasattr(func, FILE_ATTR):
            file_attr = getattr(func, FILE_ATTR)
            process_file_data(name, func, file_attr)
            delattr(cls, name)
    return cls
