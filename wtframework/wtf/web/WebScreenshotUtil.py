'''
Created on Dec 22, 2012

@author: "David Lai"
'''
from selenium.webdriver import remote
from wtframework.wtf.utils.ProjectUtils import ProjectUtils
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
        @param webdriver: WebDriver.
        @type webdriver: WebDriver
        @param file_name: Name to label this screenshot.
        @type file_name: str 
        """
        file_location = os.path.join(ProjectUtils.get_project_root() +
                                            WebScreenShotUtil.SCREEN_SHOT_LOCATION + 
                                            file_name + 
                                            ".png")

        WebScreenShotUtil.__capture_screenshot(webdriver, file_location)

    @staticmethod
    def take_reference_screenshot(webdriver, file_name):
        file_location = os.path.join(ProjectUtils.get_project_root() +
                                    WebScreenShotUtil.REFERENCE_SCREEN_SHOT_LOCATION + 
                                    file_name + 
                                    ".png")
        WebScreenShotUtil.__capture_screenshot(webdriver, file_location)

    @staticmethod
    def __capture_screenshot(webdriver, file_location):
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