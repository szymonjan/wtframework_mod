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
"""
This module contains various utility methods that assist with waiting and polling.
"""

from datetime import datetime, timedelta
import time

from six import u
from wtframework.wtf.config import WTF_TIMEOUT_MANAGER


class OperationTimeoutError(Exception):

    """
    Timeout Error
    This error is thrown when a wait function times out.
    """
    pass




def do_until(lambda_expr, timeout=WTF_TIMEOUT_MANAGER.NORMAL, sleep=0.5, message=None):
    '''
    A retry wrapper that'll keep performing the action until it succeeds.
    (main differnce between do_until and wait_until is do_until will keep trying 
    until a value is returned, while wait until will wait until the function 
    evaluates True.)

    Args:
        lambda_expr (lambda) : Expression to evaluate.

    Kwargs: 
        timeout (number): Timeout period in seconds.
        sleep (number) : Sleep time to wait between iterations
        message (str) : Provide a message for TimeoutError raised.

    Returns:
        The value of the evaluated lambda expression.

    Usage::

        do_until(lambda: driver.find_element_by_id("save").click(),
                 timeout=30,
                 sleep=0.5)

    Is equivalent to:

        end_time = datetime.now() + timedelta(seconds=30)
        while datetime.now() < end_time:
            try:
                return driver.find_element_by_id("save").click()
            except:
                pass
            time.sleep(0.5)
        raise OperationTimeoutError()
    '''
    __check_condition_parameter_is_function(lambda_expr)

    end_time = datetime.now() + timedelta(seconds=timeout)
    last_exception = None
    while datetime.now() < end_time:
        try:
            return lambda_expr()
        except Exception as e:
            last_exception = e
            time.sleep(sleep)

    if message:
        raise OperationTimeoutError(message, last_exception)
    else:
        raise OperationTimeoutError("Operation timed out.", last_exception)



def wait_until(condition, timeout=WTF_TIMEOUT_MANAGER.NORMAL, sleep=0.5, pass_exceptions=False, message=None):
    '''
    Waits wrapper that'll wait for the condition to become true.
    (main differnce between do_until and wait_until is do_until will keep trying 
    until a value is returned, while wait until will wait until the function 
    evaluates True.)

    Args:
        condition (lambda) - Lambda expression to wait for to evaluate to True.

    Kwargs:
        timeout (number) : Maximum number of seconds to wait.
        sleep (number) : Sleep time to wait between iterations.
        pass_exceptions (bool) : If set true, any exceptions raised will be re-raised up the chain.
                                Normally exceptions are ignored.
        message (str) : Optional message to pass into OperationTimeoutError if the wait times out.

    Example::

        wait_until(lambda: driver.find_element_by_id("success").is_displayed(), 
                   timeout=30,
                   sleep=0.5)

    is equivalent to::

        end_time = datetime.now() + timedelta(seconds=30)
        did_succeed = False
        while datetime.now() < end_time:
            try:
                if driver.find_element_by_id("success").is_displayed():
                    did_succeed = True
                    break;
            except:
                pass
            time.sleep(0.5)
        if not did_succeed:
            raise OperationTimeoutError()
    '''
    __check_condition_parameter_is_function(condition)

    last_exception = None
    end_time = datetime.now() + timedelta(seconds=timeout)
    while datetime.now() < end_time:
        try:
            if condition():
                return
        except Exception as e:
            if pass_exceptions:
                raise e
            else:
                last_exception = e
        time.sleep(sleep)

    if message:
        if last_exception:
            raise OperationTimeoutError(message, e)
        else:
            raise OperationTimeoutError(message)
    else:
        if last_exception:
            raise OperationTimeoutError("Operation timed out.", e)
        else:
            raise OperationTimeoutError("Operation timed out.")


def __check_condition_parameter_is_function(condition):
    # Check the condition is a callable lambda or function.
    if not hasattr(condition, '__call__'):
        raise TypeError(u("Condition argument does not appear to be a callable function.") + 
                           u("Please check if this is a properly formatted lambda/function statement."),
                           condition)
