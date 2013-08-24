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

from wtframework.wtf.config import WTF_CONFIG_READER
from wtframework.wtf.web.capture import WebScreenShotUtil
from wtframework.wtf.web.webdriver import WTF_WEBDRIVER_MANAGER
import abc
import datetime
import re


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
        Callback runs before setup. (will always get called)
        
        Args:
            test_case (TestCase) : TestCase instance associated with watched test
            test_result (TestResult) : TestReslt instance associated with watched test
        """
        pass
    
        
    def before_test(self, test_case, test_result):
        """
        Callback runs before test, but after setup. (will get called if setup succeeds)
        
        Args:
            test_case: TestCase instance associated with watched test
            test_result: TestResult instance associated with watched test

        """
        pass
    
    def after_test(self, test_case, test_result):
        """
        Callback runs after test, but before teardown (will always get called if test runs)
        
        Args:
            test_case: TestCase instance associated with watched test
            test_result: TestResult associated with watched test

        """
        pass
    
    
    def after_teardown(self, test_case, test_result):
        """
        Callback runs after tearDown. (will always get called)
        
        Args:
            test_case: TestCase associated with watched test
            test_result: TestResult associated with watched test

        """
        pass
    
    def on_test_failure(self, test_case, test_result, exception):
        """
        Runs when an unexpected test failure occurs
        
        Args:
            test_case: TestCase associated with watched test
            test_result: TestResult associated with watched test
            exception: Exception that was thrown by the failure.

        """
        pass


    def on_test_error(self, test_case, test_result, exception):
        """
        Callback runs when a test error occurs.
        
        @param test_case: TestCase associated with watched test.
        @param test_result: TestResult associated with watched test.
        @param exception: Exception raised by the test error.
        """
        pass


    def on_test_pass(self, test_case, test_result):
        """
        Callback runs when a test has passed.
        
        @param test_case: TestCase associated with watched test.
        @param test_result: TestResult associated with watched test.
        """
        pass



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
        self.exception_list = []


    def delay_failure(self, function, additional_debug_info):
        """
        Wrap a assertion call to delay test failure till after the test.
        Usage: delayed_fail_watcher.delay_failure( lambda: self.assertEquals(5, x) )

        Args:
            function (function) : Function to evaluate. 
            additional_debug_info : Execution frame reference to the failure.
            
        Return: 
            None if succeeds.  Returns a reference the exception if failed.

        """
        try:
            #run assertion.
            function()

            return None
        except Exception as e:

            if not additional_debug_info:
                self.exception_list.append(e)
            else:
                self.exception_list.append((e,additional_debug_info))
            return e


    def on_test_pass(self, test_case, test_result):
        """
        Call back method implementation of this test watcher.
        """
        if len(self.exception_list) > 0:
            raise DelayedTestFailure(*tuple(self.exception_list))



class DelayedTestFailure(AssertionError):
    "Thrown at the end of a test if there are test failure."
    
    def __init__(self, *args, **kwargs):
        super(DelayedTestFailure, self).__init__(*args, **kwargs)
        self.exception_list = args
    
    #Overriding __str__ to make the error message easier to read.
    def __str__(self, *args, **kwargs):
        exception_string = ""
        count = 0
        for exception_entry in self.exception_list:
            count += 1
            exception_string += "\nError {0}: ".format(count) + exception_entry.__str__()
        
        return AssertionError.__str__(self, *args, **kwargs) + exception_string



class CaptureScreenShotOnErrorTestWatcher(TestWatcher):
    '''
    Catures screenshot on error if the config setting is enabled.
    
    To enable this, you'll need to set in your config.yaml::
    
        selenium:
            take_screenshot: true
    
    
    '''

    def __init__(self, webdriver_provider=None, screenshot_util=None):
        '''
        Constructor.
        
        Kwargs:
            webdriver_provider: Override the default WebdriverManager instance.
            screenshot_util: Override the default screenshot util method.

        '''
        if WTF_CONFIG_READER.get("selenium.take_screenshot", True):
            self.capture_screenshot = True
        else:
            self.capture_screenshot = False
        
        if webdriver_provider == None:
            self._webdriver_provider = WTF_WEBDRIVER_MANAGER
        else:
            self._webdriver_provider = webdriver_provider

        if screenshot_util == None:
            self._screenshot_util = WebScreenShotUtil
        else:
            self._screenshot_util = screenshot_util 


    def on_test_failure(self, test_case, test_result, exception):
        """
        On test failure capture screenshot handler.
        """
        if self.capture_screenshot: self.__take_screenshot_if_webdriver_open__(test_case)


    def on_test_error(self, test_case, test_result, exception):
        """
        On test error, capture screenshot handler.
        """
        if self.capture_screenshot: self.__take_screenshot_if_webdriver_open__(test_case)


    def __generate_screenshot_filename__(self, testcase):
        '''
        Get the class name and timestamp for generating filenames
        
        Return: 
            str - File Name.

        '''
        fname = type(testcase).__name__ + "_" + testcase._testMethodName
        fname = re.sub("[^a-zA-Z_]+", "_", fname)
        #Trim test case name incase it's too long.
        fname = fname[:20]
        fmt='%y-%m-%d_%H.%M.%S_{fname}'
        return datetime.datetime.now().strftime(fmt).format(fname=fname)


    def __take_screenshot_if_webdriver_open__(self, testcase):
        '''
        Take a screenshot if webdriver is open.
        
        Args:
            testcase: TestCase

        '''
        if self._webdriver_provider.is_driver_available():
            try:
                name = self.__generate_screenshot_filename__(testcase)
                self._screenshot_util.take_screenshot(self._webdriver_provider.get_driver(), name)
                print "Screenshot taken:" + name
            except Exception as e:
                print "Unable to take screenshot. Reason: " + e.message + str(type(e))

