'''
Created on Feb 13, 2013

@author: "David Lai"
'''
from wtframework.wtf.testobjects.TestWatcher import TestWatcher


class DelayedTestFailTestWatcher(TestWatcher):
    '''
    Delayed test fail test watcher allows for the ability to call wrapped assertions.
    Assertions fails will be stored in a list, then on_test_pass(), any failures stored 
    in the list will immediately be thrown causing the test to fail.
    
    Note: this will immediately throw an exception on_test_pass(), any actions that use 
    on_test_pass() that you would like to execute should be added before this test watcher.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        print "Init"
        self.exception_list = []


    def delay_failure(self, function, additional_debug_info):
        """
        Wrap a assertion call to delay test failure till after the test.
        Usage: delayed_fail_watcher.delay_failure( lambda: self.assertEquals(5, x) )
        
        @param function: Function reference of lambda expression to be evaluated. 
        @param current_execution_frame: Pass it a frame to include in the exception to 
            aid in debugging.
        @return: None if succeeds.  Returns a reference the exception if failed.
        """
        try:
            print "delayed failure function running."
            function()
            print "delayed failure function passed."
            return None
        except Exception as e:
            print "delayed failure function failed."

            if not additional_debug_info:
                self.exception_list.append(e)
            else:
                self.exception_list.append((e,additional_debug_info))
            return e

    def on_test_pass(self, test_case, test_result):
        print "on test passed", self.exception_list
        if len(self.exception_list) > 0:
            raise DelayedTestFailure(self.exception_list)

    


class DelayedTestFailure(AssertionError):
    "Thrown at the end of a test if there are test failure."
