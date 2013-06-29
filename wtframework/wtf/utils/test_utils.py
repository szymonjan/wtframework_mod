'''
Created on Jun 28, 2013

@author: "David Lai"
'''

if __name__ == '__main__':
    pass



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
    
    @return: Returns same return as the lambda statement.  Otherwise returns None
    """
    try:
        return lambda_func()
    except Exception as e:
        print e
        return None



def do_if_match(iterator, matching_lambda_expr, lambda_to_perform, message=None):
    """
    @param iterator: Iterator set.
    @param matching_lambda_expr: Lamba expression for matching.  It should be a lambda expression that 
        takes an item from the iterator as a parameter. Returns true if match, false otherwise.
    @param lambda_to_perform: Lambda expression to perform if a match is found, it should take an item 
        from the iterator as a parameter. 
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