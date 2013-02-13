'''
Created on Dec 24, 2012

@author: "David Lai"
'''
from wtframework.wtf.testobjects.WatchedTestCase import WatchedTestCase
from wtframework.wtf.web.CaptureScreenShotOnErrorTestWatcher import \
    CaptureScreenShotOnErrorTestWatcher


class WTFBaseTest(WatchedTestCase):
    '''
    Test Cases can extend this test to additional unit test functionality such as 
    take screenshot on failure.
    '''


    def __init__(self, methodName='runTest', webdriver_provider=None, screenshot_util=None):
        super(WTFBaseTest, self).__init__(methodName)
        self._register_watcher(CaptureScreenShotOnErrorTestWatcher(webdriver_provider, screenshot_util))
    
