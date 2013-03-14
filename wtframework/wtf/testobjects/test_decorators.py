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

@author: David Lai
"""

from functools import wraps
from wtframework.wtf.data.data_management import CsvReader, WTF_DATA_MANAGER
import re

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

