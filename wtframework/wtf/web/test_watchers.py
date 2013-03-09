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

from wtframework.wtf.testobjects.test_watchers import TestWatcher
from wtframework.wtf.web.capture import WebScreenShotUtil
from wtframework.wtf.web.webdriver import WTF_WEBDRIVER_MANAGER
import datetime
import re
from wtframework.wtf.config import WTF_CONFIG_READER

class CaptureScreenShotOnErrorTestWatcher(TestWatcher):
    '''
    Catures screenshot on error if enabled.
    '''


    def __init__(self, webdriver_provider=None, screenshot_util=None):
        '''
        Constructor
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
        Runs when an unexpected test failure occurs
        @param test_case: Test case to pass in.
        @param test_case: wtframework.wtf.testobjects.TestCase
        """
        if self.capture_screenshot: self.__take_screenshot_if_webdriver_open__(test_case)
    
    def on_test_error(self, test_case, test_result, exception):
        """
        Runs when a test error occcurs.
        @param test_case: Test case to pass in.
        @param test_case: wtframework.wtf.testobjects.TestCase
        """
        if self.capture_screenshot: self.__take_screenshot_if_webdriver_open__(test_case)


    def __generate_screenshot_filename__(self, testcase):
        '''
        Get the class name and timestamp for generating filenames
        @return: File Name.
        @rtype: str
        '''
        fname = str(testcase).replace("(", "").replace(")", "").replace(" ", "_")
        fname = re.sub("[^a-zA-Z_]", "", fname)
        fmt='%y-%m-%d_%H.%M.%S_{fname}'
        return datetime.datetime.now().strftime(fmt).format(fname=fname)
    
    def __take_screenshot_if_webdriver_open__(self, testcase):
        '''
        Take a screenshot if webdriver is open.
        '''
        if self._webdriver_provider.is_driver_available():
            try:
                name = self.__generate_screenshot_filename__(testcase)
                self._screenshot_util.take_screenshot(self._webdriver_provider.get_driver(), name)
                print "Screenshot taken:" + name
            except Exception as e:
                print "Unable to take screenshot. Reason: " + e.message + str(type(e))
