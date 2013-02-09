'''
Created on Feb 8, 2013

@author: davidlai
'''
import unittest
from wtframework.wtf.testobjects.TestCase import TestCase


class TestTestCase(TestCase):
    log = []
    
    def __init__(self, method_name):
        super(TestTestCase, self).__init__(method_name)
        self.register_test_watcher(LoggerTestWatcher())
    
    def setUp(self):
        TestTestCase.log.append("setUp")
    
    def tearDown(self):
        TestTestCase.log.append("tearDown")
        
    def test_aaa_something(self):
        "Dummy test to set things up."
        TestTestCase.log.append("test")
    
    def test_zzz_test_our_real_event_sequence(self):
        "Check the dummy test's sequence of events."
        
        # Keep in mind we're running a test within a test.  It gets ugly.
        self.assertEqual(['before_setup', 'before_setup', 'setUp', 'before_test', 'before_test', 'test', 'on_test_pass', 'on_test_pass', 'after_test', 'after_test', 'tearDown', 'after_teardown', 'after_teardown', 'before_setup', 'before_setup', 'setUp', 'before_test', 'before_test'], 
                         self.log)


class LoggerTestWatcher(object):
    "This test watcher just logs actions to a list to verify order of events."
    
    log = []

    def before_setup(self, test_case, test_result):
        test_case.log.append("before_setup")
    
        
    def before_test(self, test_case, test_result):
        test_case.log.append("before_test")
    
    def after_test(self, test_case, test_result):
        test_case.log.append("after_test")
    
    
    def after_teardown(self, test_case, test_result):
        test_case.log.append("after_teardown")
    
    def on_test_failure(self, test_case, test_result, exception):
        test_case.log.append("on_test_failure")
    
    def on_test_error(self, test_case, test_result, exception):
        test_case.log.append("on_test_error")
    
    def on_test_pass(self, test_case, test_result):
        test_case.log.append("on_test_pass")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()