'''
Created on Feb 8, 2013

@author: davidlai
'''
from unittest.case import _ExpectedFailure, _UnexpectedSuccess, SkipTest
import sys
import unittest
import warnings

class TestCase(unittest.TestCase):
    '''
    This test case extends the unittest.TestCase to add support for 
    registering TestWatchers for listening on TestEvents.
    '''
    
    __wtf_test_watchers__ = []


    def register_test_watcher(self, watcher, position = -1):
        """
        Register a test watcher.
        @param watcher: A test watcher. 
        """
        self.__wtf_test_watchers__.insert(position, watcher)


    def unregister_test_watcher(self, watcher):
        """"
        Unregister a test watcher.
        """
        self.__wtf_test_watchers__.remove(watcher)


    def run(self, result=None):
        """
        Overriding the run() method to insert our screenshot handler.
        
        Most of this method is a copy of the TestCase.run() method source.
        """
        orig_result = result
        if result is None:
            result = self.defaultTestResult()
            startTestRun = getattr(result, 'startTestRun', None)
            if startTestRun is not None:
                startTestRun()

        self._resultForDoCleanups = result
        result.startTest(self)

        testMethod = getattr(self, self._testMethodName)
        if (getattr(self.__class__, "__unittest_skip__", False) or
            getattr(testMethod, "__unittest_skip__", False)):
            # If the class or method was skipped.
            try:
                skip_why = (getattr(self.__class__, '__unittest_skip_why__', '')
                            or getattr(testMethod, '__unittest_skip_why__', ''))
                self._addSkip(result, skip_why)
            finally:
                result.stopTest(self)
            return
        try:
            success = False
            try:
                # Run our test watcher actions.
                for test_watcher in self.__wtf_test_watchers__:
                    test_watcher.before_setup(self, result)
                # Run test setup.
                self.setUp()
            except SkipTest as e:
                self._addSkip(result, str(e))
            except KeyboardInterrupt:
                raise
            except:
                result.addError(self, sys.exc_info())
            else:
                try:
                    # Run our test watcher actions.
                    for test_watcher in self.__wtf_test_watchers__:
                        test_watcher.before_test(self, result)
                    # Run our test
                    testMethod()
                    
                    # Run our test watcher actions.
                    for test_watcher in self.__wtf_test_watchers__:
                        test_watcher.on_test_pass(self, result)
                    
                except KeyboardInterrupt:
                    raise
                except self.failureException as e:
                    result.addFailure(self, sys.exc_info())

                    # Run our test watcher actions.
                    for test_watcher in self.__wtf_test_watchers__:
                        test_watcher.on_test_failure(self, result, e)
                    
                except _ExpectedFailure as e:
                    addExpectedFailure = getattr(result, 'addExpectedFailure', None)
                    if addExpectedFailure is not None:
                        addExpectedFailure(self, e.exc_info)
                    else:
                        warnings.warn("TestResult has no addExpectedFailure method, reporting as passes",
                                      RuntimeWarning)
                        result.addSuccess(self)

                except _UnexpectedSuccess:
                    addUnexpectedSuccess = getattr(result, 'addUnexpectedSuccess', None)
                    if addUnexpectedSuccess is not None:
                        addUnexpectedSuccess(self)
                    else:
                        warnings.warn("TestResult has no addUnexpectedSuccess method, reporting as failures",
                                      RuntimeWarning)
                        result.addFailure(self, sys.exc_info())

                except SkipTest as e:
                    self._addSkip(result, str(e))
                except Exception as e:
                    result.addError(self, sys.exc_info())
                    
                    # Run our test watcher actions.
                    for test_watcher in self.__wtf_test_watchers__:
                        test_watcher.on_test_error(self, result, e)
                else:
                    success = True

                try:
                    # Run our test watcher actions.
                    for test_watcher in self.__wtf_test_watchers__:
                        test_watcher.after_test(self, result)
                    
                    # Do tear down.
                    self.tearDown()
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    result.addError(self, sys.exc_info())
                    success = False
                    
                    # Run our test watcher actions.
                    for test_watcher in self.__wtf_test_watchers__:
                        test_watcher.on_test_error(self, result, e)
                finally:
                    # Run our test watcher actions.
                    for test_watcher in self.__wtf_test_watchers__:
                        test_watcher.after_teardown(self, result)

            
            cleanUpSuccess = self.doCleanups()
            success = success and cleanUpSuccess
            if success:
                result.addSuccess(self)
        finally:
            result.stopTest(self)
            if orig_result is None:
                stopTestRun = getattr(result, 'stopTestRun', None)
                if stopTestRun is not None:
                    stopTestRun()
    
        