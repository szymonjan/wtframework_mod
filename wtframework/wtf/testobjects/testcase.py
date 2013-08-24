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
from unittest.case import _ExpectedFailure, _UnexpectedSuccess, SkipTest
import sys
import unittest2
import warnings

class WatchedTestCase(unittest2.TestCase):
    '''
    This test case extends the unittest.TestCase to add support for 
    registering TestWatchers for listening on TestEvents.
    '''
    
    def __init__(self, *args, **kwargs):
        self.__wtf_test_watchers__ = []
        super(WatchedTestCase, self).__init__(*args, **kwargs)


    # '_' prefix is added to hide it form nosetest
    def _register_watcher(self, watcher, position = -1):
        """
        Register a test watcher.

        Args:
            watcher: A test watcher to register.
        
        Kwargs:
            position: position in execution queue to insert this watcher.
        """
        self.__wtf_test_watchers__.insert(position, watcher)


    # '_' prefix is added to hide it form nosetest
    def _unregister_watcher(self, watcher):
        """"
        Unregister a test watcher.
        
        Args:
            watcher : Reference to TestWatcher to unregister.
        """
        self.__wtf_test_watchers__.remove(watcher)


    def get_log(self):
        """
        Get a log of events fired.
        
        Returns:
            list - list of string names of events fired.
        """
        log = []
        for watcher in self.__wtf_test_watchers__:
            log = watcher.get_log() + log
        return log


    def run(self, result=None):
        """
        Overriding the run() method to insert calls to our TestWatcher call-backs.

        Most of this method is a copy of the unittest.TestCase.run() method source.
        
        Kwargs:
            result: TestResult object.
        """
        orig_result = result
        if result is None:
            result = self.defaultTestResult()
            startTestRun = getattr(result, 'startTestRun', None)
            if startTestRun is not None:
                startTestRun()

        did_tear_down_execute = False # Track if clean up was run, so we can run clean up if setup failed.

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
            except SkipTest, e:
                self._addSkip(result, str(e))
            except Exception:
                result.addError(self, sys.exc_info())
            else:
                try:
                    # Run our test watcher actions.
                    for test_watcher in self.__wtf_test_watchers__:
                        test_watcher.before_test(self, result)

                    # Run our test
                    testMethod()
                    
                    # Run our test watcher post test actions.
                    for test_watcher in self.__wtf_test_watchers__:
                        test_watcher.on_test_pass(self, result)

                except self.failureException as e:
                    result.addFailure(self, sys.exc_info())
                    
                    # Run our test watcher on fail actions.
                    for test_watcher in self.__wtf_test_watchers__:
                        test_watcher.on_test_failure(self, result, e)

                except _ExpectedFailure, e:
                    addExpectedFailure = getattr(result, 'addExpectedFailure', None)
                    if addExpectedFailure is not None:
                        addExpectedFailure(self, e.exc_info)
                    else: 
                        warnings.warn("Use of a TestResult without an addExpectedFailure method is deprecated", 
                                      DeprecationWarning)
                        result.addSuccess(self)
                except _UnexpectedSuccess:
                    addUnexpectedSuccess = getattr(result, 'addUnexpectedSuccess', None)
                    if addUnexpectedSuccess is not None:
                        addUnexpectedSuccess(self)
                    else:
                        warnings.warn("Use of a TestResult without an addUnexpectedSuccess method is deprecated", 
                                      DeprecationWarning)
                        result.addFailure(self, sys.exc_info())
                except SkipTest, e:
                    self._addSkip(result, str(e))
                except Exception as e:
                    result.addError(self, sys.exc_info())
                    
                    # Run our test watcher on error actions.
                    for test_watcher in self.__wtf_test_watchers__:
                        test_watcher.on_test_error(self, result, e)
                else:
                    success = True

                try:
                    did_tear_down_execute = True
                    # Run our test watcher after test actions.
                    for test_watcher in self.__wtf_test_watchers__:
                        test_watcher.after_test(self, result)

                    # Do tear down.
                    self.tearDown()
                except Exception:
                    result.addError(self, sys.exc_info())
                    success = False
                    
                finally: # Run our test watcher actions for after tear down..
                    for test_watcher in self.__wtf_test_watchers__:
                        test_watcher.after_teardown(self, result)

            cleanUpSuccess = self.doCleanups()
            success = success and cleanUpSuccess
            if success:
                result.addSuccess(self)
        finally:
            # Execute tear down if it did not get executed.
            if not did_tear_down_execute:
                # Run our test watcher after test actions.
                try:
                    for test_watcher in self.__wtf_test_watchers__:
                        test_watcher.after_test(self, result)
                    self.tearDown()
                except:
                    pass # do nothing, test case would already failed and failure is already handled.
                finally: # Run our test watcher actions for after tear down..
                    for test_watcher in self.__wtf_test_watchers__:
                        test_watcher.after_teardown(self, result)

            # Remove test watchers.  For some strange reason these apply to all test 
            # cases, not just the currently running one.  So we remove them here.
            self.__wtf_test_watchers__ = []

            result.stopTest(self)
            if orig_result is None:
                stopTestRun = getattr(result, 'stopTestRun', None)
                if stopTestRun is not None:
                    stopTestRun()
