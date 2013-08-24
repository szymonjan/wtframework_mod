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

from selenium.webdriver import remote
from wtframework.wtf.utils.project_utils import ProjectUtils
import base64
import os

class WebScreenShotUtil():
    '''
    Utilities for taking screenshots in Selenium Webdriver.
    '''

    SCREEN_SHOT_LOCATION = "screenshots/"
    REFERENCE_SCREEN_SHOT_LOCATION = "reference-screenshots/"

    @staticmethod
    def take_screenshot(webdriver, file_name):
        """
        Captures a screenshot.
        
        Args:
            webdriver (WebDriver) - Selenium webdriver.
            file_name (str) - File name to save screenshot as.

        """
        file_location = os.path.join(ProjectUtils.get_project_root() +
                                            WebScreenShotUtil.SCREEN_SHOT_LOCATION + 
                                            file_name + 
                                            ".png")

        WebScreenShotUtil.__capture_screenshot(webdriver, file_location)

    @staticmethod
    def take_reference_screenshot(webdriver, file_name):
        """
        Captures a screenshot as a reference screenshot.
        
        Args:
            webdriver (WebDriver) - Selenium webdriver.
            file_name (str) - File name to save screenshot as.
        """
        file_location = os.path.join(ProjectUtils.get_project_root() +
                                    WebScreenShotUtil.REFERENCE_SCREEN_SHOT_LOCATION + 
                                    file_name + 
                                    ".png")
        WebScreenShotUtil.__capture_screenshot(webdriver, file_location)


    @staticmethod
    def __capture_screenshot(webdriver, file_location):
        "Capture a screenshot"
        if isinstance(webdriver, remote.webdriver.WebDriver):
            # If this is a remote webdriver.  We need to transmit the image data 
            # back across system boundries as a base 64 encoded string so it can 
            # be decoded back on the local system and written to disk.
            base64_data = webdriver.get_screenshot_as_base64()
            screenshot_data = base64.decodestring(base64_data)
            screenshot_file = open(file_location, "w")
            screenshot_file.write(screenshot_data)
            screenshot_file.close()
        else:
            webdriver.save_screenshot(file_location)
