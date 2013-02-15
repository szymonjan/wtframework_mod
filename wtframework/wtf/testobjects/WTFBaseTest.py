'''
Created on Dec 24, 2012

@author: "David Lai"
'''
from wtframework.wtf.testobjects.WatchedTestCase import WatchedTestCase
from wtframework.wtf.web.CaptureScreenShotOnErrorTestWatcher import \
    CaptureScreenShotOnErrorTestWatcher
from wtframework.wtf.testobjects.DelayedTestFailTestWatcher import DelayedTestFailTestWatcher
import inspect


class WTFBaseTest(WatchedTestCase):
    '''
    Test Cases can extend this test to additional unit test functionality such as 
    take screenshot on failure.
    '''

    def __init__(self, methodName='runTest', webdriver_provider=None, screenshot_util=None):
        super(WTFBaseTest, self).__init__(methodName)
        self._register_watcher(CaptureScreenShotOnErrorTestWatcher(webdriver_provider, screenshot_util))

        # Note this watcher should be registered after all other watchers that use 
        # on_test_passed() event.
        self._delayed_test_watcher = DelayedTestFailTestWatcher()
        self._register_watcher(self._delayed_test_watcher)

    def assertWithDelayedFailure(self, assert_method, *params):
        """
        Cause an assertion failure to be delayed till the end of the test.
        
        Usage:
            self.assertWithDelayedFailure(self.AssertEquals, 100, percent)
        @param assert_method: Reference to assert method.
        @param *params: parameters to pass into assert method.
        """
        frame = None
        try:
            #attempt to get parent frames
            frame = inspect.getouterframes(inspect.currentframe())[1]
        except:
            pass #oh well, we couldn't get it.
        
        assert_func = lambda: assert_method(*params)
        generated_exception = self._delayed_test_watcher.delay_failure(assert_func, frame)
        


        if not generated_exception != None:
            # Call our on_fail for our test watchers.  So we can trigger our screen 
            # capture at moment of failure.
            for test_watcher in self.__wtf_test_watchers__:
                test_watcher.on_test_failure(self, self._resultForDoCleanups, generated_exception)

