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
        print e
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

        numbers = [1, 2, 3, 4, 5, 6]
        matcher = lambda num: num % 2 == 0
        action = lambda num: print num
        do_if_match(numbers, matcher, action) # prints 2
    
    Is equivalent to:

        numbers = [1, 2, 3, 4, 5, 6]
        for num in numbers:
            if num % 2 == 0:
                print num

    """
    if message is None:
        message = "Unable to find matching item in " + str(iterator)

    for item in iterator:
        if matching_lambda_expr(item):
            return lambda_to_perform(item)

    raise NoMatchError(message)



class NoMatchError(RuntimeError):
    "Raised if no match is found."
    pass

