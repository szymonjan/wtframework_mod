'''
Created on Dec 17, 2012

@author: "David Lai"
'''
from mox import Mox
from selenium.webdriver import phantomjs
from selenium.webdriver.remote.webelement import WebElement
from wtframework.wtf.web.WebDriverFactory import WebDriverFactory
from wtframework.wtf.web.WebDriverManager import WebDriverManager
import unittest


class TestWebDriverProvider(unittest.TestCase):

    _mocker = None

    def setUp(self):
        #create an instance of Mox() to mock out config.
        self._mocker = Mox()


    def tearDown(self):
        # reset our singleton providers.
        WebDriverManager.clear_instance()
        self._mocker = None


    def test_getInstance_ReturnsSingleton(self):
        '''
        Test we return a singleton instance of the webdriver provider.
        '''
        webdriverfactory_mock = self._mocker.CreateMock(WebDriverFactory)
        webdriverfactory_mock.create_webdriver().AndReturn(None)
        self._mocker.ReplayAll()
        
        wdp1 = WebDriverManager.get_instance()
        wdp2 = WebDriverManager.get_instance()
        self.assertTrue(isinstance(wdp1, WebDriverManager), 'Returned class does not match expected')
        self.assertEqual(id(wdp1), id(wdp2), 'Returned instnace is not the same.')

    def test_getDriver_ReturnsSingletonSeleniumWebdriver(self):
        '''
        Test we return a single instance of selenium webdriver.
        '''
        mock_element = self._mocker.CreateMock(WebElement)
        mock_element.send_keys("Hello World").AndReturn(None)
        webdriver_mock = self._mocker.CreateMock(phantomjs.webdriver.WebDriver)
        webdriver_mock.get("http://www.google.com").AndReturn(None)
        webdriver_mock.find_element_by_name('q').AndReturn(mock_element)
        webdriverfactory_mock = self._mocker.CreateMock(WebDriverFactory)
        webdriverfactory_mock.create_webdriver().AndReturn(webdriver_mock)
        self._mocker.ReplayAll()

        webdriver_provider = WebDriverManager(webdriverfactory_mock)

        # Perform singleton tests
        driver1 = webdriver_provider.get_driver()
        driver2 = webdriver_provider.get_driver()
        self.assertIsNotNone(driver1, 'object is not webdriver.')
        self.assertEqual(id(driver1), id(driver2), 'Webdriver instance should be singleton.')

        # Do a small test by grabbing google's screen to exercise the webdriver interface.
        driver1.get("http://www.google.com")
        element = driver1.find_element_by_name('q') # Q is the name google use for the query field.
        element.send_keys("Hello World")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()