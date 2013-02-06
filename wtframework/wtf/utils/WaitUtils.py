'''
Created on Dec 28, 2012

@author: "David Lai"
'''
from datetime import datetime, timedelta
from wtframework.wtf.config.TimeOutManager import WTF_TIMEOUT_MANAGER
import time

class WaitUtils():
    '''
    Utility class with various static methods for working with web.
    '''

    @staticmethod
    def wait_until(condition, timeout=WTF_TIMEOUT_MANAGER.NORMAL, sleep=0.5, pass_exceptions=False):
        '''
        Waits until URL matches the expression.
        @param condition: Lambda expression to wait on.  Lambda expression 
        should return true when conditions is met.
        @type condition: lambda
        @param timeout: Timeout period in seconds.
        @rtype: int
        '''
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

        raise OperationTimeoutError("Operation timed out.")

class OperationTimeoutError(Exception):
    "Timeout Error"
    pass