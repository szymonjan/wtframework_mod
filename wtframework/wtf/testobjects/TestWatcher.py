'''
Created on Feb 8, 2013

@author: davidlai
'''
import abc

class TestWatcher(object):
    '''
    TestWatcher classes are classes that can be registered to a test 
    case and listen to events in the TestCase such as a test failing 
    or a test succeeding, and perform actions.
    
    To use TestWatcher, extend this test watcher.  Override the methods 
    corresponding to the events you are interested in.  Then you can 
    attach it to a wtframework.wtf.testobjects.TestCase using the 
    'register_test_watcher() method.
    
    Note: Exceptions in TestWatcher are not caught by the test runner.
    So it is possible to use the TestWatcher to trigger a failure.  This 
    is useful if you want to create a rule that triggered a failre if 
    certain conditions are not met.
    '''
    __metaclass__ = abc.ABCMeta
    
    

    def before_setup(self, test_case, test_result):
        """
        Runs before setup. (will always get called)
        @param test_case: Test case to pass in.
        @param test_case: wtframework.wtf.testobjects.TestCase
        """
        pass
    
        
    def before_test(self, test_case, test_result):
        """
        Runs before test, but after setup. (will get called if setup succeeds)
        @param test_case: Test case to pass in.
        @param test_case: wtframework.wtf.testobjects.TestCase
        """
        pass
    
    def after_test(self, test_case, test_result):
        """
        Runs after test, but before teardown (will always get called if test runs)
        @param test_case: Test case to pass in.
        @param test_case: wtframework.wtf.testobjects.TestCase
        """
        pass
    
    
    def after_teardown(self, test_case, test_result):
        """
        Runs after teardown. (will always get called)
        @param test_case: Test case to pass in.
        @param test_case: wtframework.wtf.testobjects.TestCase
        """
        pass
    
    def on_test_failure(self, test_case, test_result, exception):
        """
        Runs when an unexpected test failure occurs
        @param test_case: Test case to pass in.
        @param test_case: wtframework.wtf.testobjects.TestCase
        """
        pass
    
    def on_test_error(self, test_case, test_result, exception):
        """
        Runs when a test error occcurs.
        @param test_case: Test case to pass in.
        @param test_case: wtframework.wtf.testobjects.TestCase
        """
        pass
    
    def on_test_pass(self, test_case, test_result):
        """
        Runs when a test has passed.
        @param test_case: Test case to pass in.
        @param test_case: wtframework.wtf.testobjects.TestCase
        """
        pass