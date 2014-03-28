##########################################################################
# This file is part of WTFramework.
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
from wtframework.wtf import _wtflog
from six import u
"""
This module defines some wrapper functions.
"""


def do_and_ignore(lambda_func):
    """
    Perform the given function, but only log the error that's printed out.
    Use this function to wrap method calls you would normally do in a try/raise 
    block, but do not care about the results.

    Args:
        lambda_func (function) : Lambda function to execute.

    Returns:
        Returns same return as the lambda statement.  Otherwise returns None

    Usage::

        do_and_ignore(lambda: driver.find_element_by_id("logoutButton").click())

    is equivalent to::

        try:
            driver.find_element_by_id("logoutButton").click()
        except Exception as e:
            print e

    This function is useful for wrapping cleanup calls, since it'll ignore any errors 
    and keeps the test moving along.

    """
    try:
        return lambda_func()
    except Exception as e:
        try:
            print e
        except:
            _wtflog.debug("unknown error")
        return None


def do_if_match(iterator, matching_lambda_expr, lambda_to_perform, message=None):
    """
    Loops through an iterator, and for each matching lambda, perform the action associated.

    Args:
        iterator: Iterator to loop through.
        matching_lambda_expr (lambda): Lamba expression for matching. Lambda should be in the 
                                        It should be a lambda expression that 
                                        takes an item from the iterator as a parameter. 
                                        Returns true if match, false otherwise.
        lambda_to_perform: Lambda expression to perform if a match is found, it should take an item 
                            from the iterator as a parameter.


    Example::

        numbers = [1, 3, 4, 5, 6]
        matcher = lambda num: num % 2 == 0
        
        def target_action(item):
            print("The magic number is", item)

        do_if_match(numbers, matcher, target_action) # Prints "The magic number is 4"



    Is equivalent to:

        numbers = [1, 2, 3, 4, 5, 6]
        for num in numbers:
            if num % 2 == 0:
                print num

    """
    if message is None:
        message = u("Unable to find matching item in {0}").format(iterator)

    for item in iterator:
        if matching_lambda_expr(item):
            return lambda_to_perform(item)

    raise NoMatchError(message)


def find_dictonary_in(search_for_dictionary, haystack_of_dictionaries):
    """
    Searches a list or iterator of dictionaries for an entry that contains the matching matching entries 
    to the search dictionary.
    
    Args:
        search_for (dictionary): Dictionary contains key/value pairs to match.
        haystack (iterator): An iterator of dictionaries
    
    Returns:
        Returns the matching entry.  Otherwise returns None


    Usage::
    
        targets = [
            {'first':'Sarah', 'last':'Connor', 'gender':'female'},
            {'first':'John', 'last':'Connor', 'gender':'male'},
            {'first':'Waldo', 'last':'Smith', 'gender':'male'},
        ]
        look_for = {'first':'John', 'last':'Connor'}
        find_dictonary_in(look_for, targets) # Returns {'first':'John', 'last':'Connor', 'gender':'male'}

    """
    for a_dictionary in haystack_of_dictionaries:
        match_failed = False

        for key in search_for_dictionary.keys():
            try:
                if a_dictionary[key] != search_for_dictionary[key]:
                    match_failed = True
            except:
                # the entry in the haystack is missing the key.
                match_failed = True

        if not match_failed:
            return a_dictionary

    return None



class NoMatchError(RuntimeError):

    "Raised if no match is found."
    pass
