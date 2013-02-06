'''
Created on Dec 21, 2012

@author: "David Lai"
'''
from mox import Mox
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from wtframework.wtf.config.ConfigReader import ConfigReader
from wtframework.wtf.web.PageObject import PageObject, \
    InvalidPageError
import unittest


class TestPageObject(unittest.TestCase):
    '''
    Unit test of the PageObject Class
    '''


    def test_validatePage_GetsCalledDuringInit(self):
        '''
        Test the validate page and init elements is called when instantiating a page object.
        
        Note: This test is normally commented out since it launches webbrowsers.
        '''
        # Mock a webdriver that looks like it's viewing yahoo
        mox = Mox()
        config_reader = mox.CreateMock(ConfigReader)
        config_reader.get_value("selenium.take_reference_screenshot").AndReturn(False)
        driver = mox.CreateMock(WebDriver)
        driver.get("http://www.yahoo.com").AndReturn(None)
        driver.current_url = "http://www.yahoo.com"
        mox.ReplayAll()
        driver.get("http://www.yahoo.com")
        try:
            # Check we get an Invalid Page error.
            GoogleTestPageObj(driver, config_reader=config_reader)
            self.fail("Should of thrown exception.")
        except InvalidPageError:
            pass
        except Exception as e:
            self.fail("Should throw an InvalidPageError, thrown was: " + str(type(e)))

        #Mock a WebDriver that looks like it's returning google.
        mox.ResetAll()
        config_reader.get_value("selenium.take_reference_screenshot").AndReturn(False)
        driver.get("http://www.google.com").AndReturn(None)
        driver.current_url = "http://www.google.com"
        element = mox.CreateMock(WebElement)
        element.send_keys("hello world").AndReturn(None)
        # Create our 'q' element to test our init_Elements in PageObject.
        driver.find_element_by_name("q").AndReturn(element)

        driver.close().AndReturn(None)
        mox.ReplayAll()

        #check if our Page object instantiates like normal
        driver.get("http://www.google.com")
        google_page = GoogleTestPageObj(driver, config_reader=config_reader)
        # Check that the init_Elements locates our fake 'q' search bar.
        google_page.enter_query("hello world")
        driver.close()



class GoogleTestPageObj(PageObject):
    "test page"
    def _validate_page(self, webdriver):
        
        current_url = webdriver.current_url

        if not "google" in current_url:
            raise InvalidPageError()

    query_field = lambda self: self.webdriver.find_element_by_name('q')
    not_found_field = lambda self: self.webdriver.find_element_by_name('xx')
    
    def enter_query(self, query):
        self.query_field().send_keys(query)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
