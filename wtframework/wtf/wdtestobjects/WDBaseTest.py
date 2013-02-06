'''
Created on Dec 24, 2012

@author: "David Lai"
'''
from unittest.case import _ExpectedFailure, _UnexpectedSuccess, SkipTest
from wtframework.wtf.web.WebDriverProvider import WebDriverProvider
from wtframework.wtf.web.WebScreenshotUtil import WebScreenShotUtil
import datetime
import sys
import unittest
import warnings


class WDBaseTest(unittest.TestCase):
    '''
    Test Cases can extend this test to additional unit test functionality such as 
    take screenshot on failure.
    '''

    # Note: There are no unit tests for this class as this class extends TestCase,
    # and by sub-classing this, it automatically becomes a failed test that runs.
    # This is best tested manually by running a failed test.

    _webdriver_provider = None
    _screenshot_util = None

    def __init__(self, methodName='runTest', webdriver_provider=None, screenshot_util=None):
        super(WDBaseTest, self).__init__(methodName)
        
        if webdriver_provider == None:
            self._webdriver_provider = WebDriverProvider.get_instance()
        else:
            self._webdriver_provider = webdriver_provider

        if screenshot_util == None:
            self._screenshot_util = WebScreenShotUtil
        else:
            self._screenshot_util = screenshot_util 

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
                self.setUp()
            except SkipTest as e:
                self._addSkip(result, str(e))
            except KeyboardInterrupt:
                raise
            except:
                result.addError(self, sys.exc_info())
            else:
                try:
                    testMethod()
                except KeyboardInterrupt:
                    raise
                except self.failureException:
                    # Take Screenshot on test failure.
                    self.__take_screenshot_if_webdriver_open__()
                    result.addFailure(self, sys.exc_info())
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
                except:
                    # Take screenshot on error.
                    self.__take_screenshot_if_webdriver_open__()
                    result.addError(self, sys.exc_info())
                else:
                    success = True

                try:
                    self.tearDown()
                except KeyboardInterrupt:
                    raise
                except:
                    result.addError(self, sys.exc_info())
                    success = False

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


    def __generate_screenshot_filename__(self):
        '''
        Get the class name and timestamp for generating filenames
        @return: File Name.
        @rtype: str
        '''
        fname = str(self).replace("(", "").replace(")", "").replace(" ", "_")
        fmt='%y-%m-%d_%H.%M.%S_{fname}'
        return datetime.datetime.now().strftime(fmt).format(fname=fname)
    
    def __take_screenshot_if_webdriver_open__(self):
        '''
        Take a screenshot if webdriver is open.
        '''
        try:
            if self._webdriver_provider.is_driver_available():
                name = self.__generate_screenshot_filename__()
                self._screenshot_util.take_screenshot(self._webdriver_provider.get_driver(), name)
                print "Screenshot taken:" + name
        except Exception as e:
            print "Unable to take screenshot. Reason: " + e.message + str(type(e))