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

from wtframework.wtf.testobjects.test_watchers import DelayedTestFailTestWatcher, \
    CaptureScreenShotOnErrorTestWatcher
from wtframework.wtf.testobjects.testcase import WatchedTestCase
import inspect


class WTFBaseTest(WatchedTestCase):
    '''
    Test can extend this basetest to add additional unit test functionality such as 
    take screenshot on failure.
    '''

    def __init__(self, methodName='runTest', webdriver_provider=None, screenshot_util=None):
        """
        Constructor matches that of UnitTest2 test case, but modified to allow passing in 
        a ScreenShot utility and register delayed test watchers.

        Kwargs:
            methodName (str) : Test method name.
            webdriver_provider (WebdriverManager) : Default webdriver provider.
            screenshot_util (CaptureScreenShotOnErrorTestWatcher) : Screenshot capture utility.

        """
        super(WTFBaseTest, self).__init__(methodName)
        self._register_watcher(CaptureScreenShotOnErrorTestWatcher(webdriver_provider, screenshot_util))
        

        # Note this watcher should be registered after all other watchers that use 
        # on_test_passed() event.
        self._delayed_test_watcher = DelayedTestFailTestWatcher()
        self._register_watcher(self._delayed_test_watcher)


    def assertWithDelayedFailure(self, assert_method, *args, **kwargs):
        """
        Cause an assertion failure to be delayed till the end of the test.
        
        Args:
            assert_method (function) - Assert method to run.
            args - arguments to pass into the assert method.

        Kwargs:
            kwargs - additional kwargs to pass into the assert method.


        Will assert if percent == 100 at the end of the test.::
        
            self.assertWithDelayedFailure(self.AssertEquals, 100, percent)

        """
        frame = None
        try:
            #attempt to get parent frames
            frame = inspect.getouterframes(inspect.currentframe())[1]
        except:
            pass #oh well, we couldn't get it.
        
        assert_func = lambda: assert_method(*args, **kwargs)
        generated_exception = self._delayed_test_watcher.delay_failure(assert_func, frame)


        if generated_exception:
            # Call our on_fail for our test watchers.  So we can trigger our screen 
            # capture at moment of failure.
            for test_watcher in self.__wtf_test_watchers__:
                test_watcher.on_test_failure(self, self._resultForDoCleanups, generated_exception)

