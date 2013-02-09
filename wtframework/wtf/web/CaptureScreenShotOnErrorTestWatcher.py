'''
Created on Feb 8, 2013

@author: davidlai
'''
from wtframework.wtf.testobjects.TestWatcher import TestWatcher
from wtframework.wtf.web.WebScreenshotUtil import WebScreenShotUtil
from wtframework.wtf.web.WebDriverManager import WTF_WEBDRIVER_MANAGER
import datetime
import re
from wtframework.wtf.config.ConfigReader import WTF_CONFIG_READER

class CaptureScreenShotOnErrorTestWatcher(TestWatcher):
    '''
    Catures screenshot on error if enabled.
    '''

    capture_screenshot = False
    
    _webdriver_provider = None
    _screenshot_util = None

    def __init__(self, webdriver_provider=None, screenshot_util=None):
        '''
        Constructor
        '''
        if WTF_CONFIG_READER.get_value_or_default("selenium.take_screenshot", True):
            self.capture_screenshot = True

        
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
        Runs when an unexpected test failure occurs
        @param test_case: Test case to pass in.
        @param test_case: wtframework.wtf.testobjects.TestCase
        """
        if self.capture_screenshot: self.__take_screenshot_if_webdriver_open__()
    
    def on_test_error(self, test_case, test_result, exception):
        """
        Runs when a test error occcurs.
        @param test_case: Test case to pass in.
        @param test_case: wtframework.wtf.testobjects.TestCase
        """
        if self.capture_screenshot: self.__take_screenshot_if_webdriver_open__()


    def __generate_screenshot_filename__(self):
        '''
        Get the class name and timestamp for generating filenames
        @return: File Name.
        @rtype: str
        '''
        fname = str(self).replace("(", "").replace(")", "").replace(" ", "_")
        fname = re.sub("[^a-zA-Z_]", "", fname)
        fmt='%y-%m-%d_%H.%M.%S_{fname}'
        return datetime.datetime.now().strftime(fmt).format(fname=fname)
    
    def __take_screenshot_if_webdriver_open__(self):
        '''
        Take a screenshot if webdriver is open.
        '''
        if self._webdriver_provider.is_driver_available():
            try:
                name = self.__generate_screenshot_filename__()
                self._screenshot_util.take_screenshot(self._webdriver_provider.get_driver(), name)
                print "Screenshot taken:" + name
            except Exception as e:
                print "Unable to take screenshot. Reason: " + e.message + str(type(e))
