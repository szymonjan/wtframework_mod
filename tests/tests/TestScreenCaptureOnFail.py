'''
Created on Feb 9, 2013

@author: davidlai
'''
import unittest
from wtframework.wtf.testobjects.WTFBaseTest import WTFBaseTest
from wtframework.wtf.web.WebDriverManager import WTF_WEBDRIVER_MANAGER


class TestScreenCaptureOnFail(WTFBaseTest):

    # Comment out decorator to manually test the screen capture.
    @unittest.expectedFailure
    def test_fail(self):
        driver = WTF_WEBDRIVER_MANAGER.get_driver()
        driver.get('http://www.google.com')
        self.fail()
        #Check your /screenshots folder for a screenshot.

    # Comment out decorator to manually test the screen capture.
    @unittest.expectedFailure
    def test_assert(self):
        driver = WTF_WEBDRIVER_MANAGER.get_driver()
        driver.get('http://www.google.com')
        self.assertEqual(1, 2)
        #Check your /screenshots folder for a screenshot.

    # Comment out decorator to manually test the screen capture.
    @unittest.expectedFailure
    def test_error(self):
        driver = WTF_WEBDRIVER_MANAGER.get_driver()
        driver.get('http://www.google.com')
        raise RuntimeError()
        #Check your /screenshots folder for a screenshot.

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()