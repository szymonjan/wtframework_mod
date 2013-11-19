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
This module contains various utility methods that assist with waiting and polling.
"""

from datetime import datetime, timedelta
from wtframework.wtf.config import WTF_TIMEOUT_MANAGER
import time


class OperationTimeoutError(Exception):
    """
    Timeout Error
    This error is thrown when a wait function times out.
    """
    pass


def wait_until(condition, timeout=WTF_TIMEOUT_MANAGER.NORMAL, sleep=0.5, pass_exceptions=False, message=None):
    '''
    Waits wrapper that'll wait for the condition to become true.
    
    Args:
        condition (lambda) - Lambda expression to wait for to evaluate to True.
    
    Kwargs:
        timeout (number) : Maximum number of seconds to wait.
        sleep (number) : Sleep time to wait between iterations.
        pass_exceptions (bool) : If set true, any exceptions raised will be re-raised up the chain.
                                Normally exceptions are ignored.
        message (str) : Optional message to pass into OperationTimeoutError if the wait times out.

    Example::

        wait_until(lambda: driver.find_element_by_id("success").is_displayed(), timeout=30)
    
    is equivalent to::

        end_time = datetime.now() + timedelta(seconds=30)
        while datetime.now() < end_time:
            try:
                if driver.find_element_by_id("success").is_displayed():
                    break;
            except:
                pass
            time.sleep(0.5)

    '''
    if not hasattr(condition, '__call__'):
        raise RuntimeError("Condition argument does not appear to be a callable function." + 
                           "Please check if this is a properly formatted lambda statement.", 
                           condition)
    end_time = datetime.now() + timedelta(seconds = timeout)
    while datetime.now() < end_time:
        try:
            if condition():
                return
        except Exception as e:
            if pass_exceptions:
                raise e
            else:
                pass
        time.sleep(sleep)
    
    if message:
        raise OperationTimeoutError(message)
    else:
        raise OperationTimeoutError("Operation timed out.")


def do_until(lambda_expr, timeout=WTF_TIMEOUT_MANAGER.NORMAL, sleep=0.5, message=None):
    '''
    A retry wrapper that'll keep performing the action until it succeeds.
    
    Args:
        lambda_expr (lambda) : Expression to evaluate.
    
    Kwargs: 
        timeout (number): Timeout period in seconds.
        sleep (number) : Sleep time to wait between iterations
        message (str) : Provide a message for TimeoutError raised.
    
    Returns:
        The value of the evaluated lambda expression.

    Usage::

        do_until(lambda: driver.find_element_by_id("save").click())
    
    Is equivalent to:

        end_time = datetime.now() + timedelta(seconds=30)
        while datetime.now() < end_time:
            try:
                driver.find_element_by_id("save").click()
                break;
            except:
                pass
            time.sleep(0.5)

    '''
    end_time = datetime.now() + timedelta(seconds = timeout)
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

