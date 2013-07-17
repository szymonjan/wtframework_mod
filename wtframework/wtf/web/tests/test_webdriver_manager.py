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

from interruptingcow import timeout
from mockito.matchers import any
from mockito.mockito import when, mock, verify
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from wtframework.wtf.config import ConfigReader
from wtframework.wtf.web.webdriver import WebDriverFactory, WebDriverManager
import threading
import unittest


class TestWebDriverManager(unittest.TestCase):


    
    def test_getDriver_ReturnsSingletonSeleniumWebdriver(self):
        '''
        Test we return a single instance of selenium webdriver.
        '''
        mock_element = mock(WebElement)
        when(mock_element).send_keys(any(str)).thenReturn(None)
        webdriver_mock = mock(WebDriver)
        when(webdriver_mock).get("http://www.google.com").thenReturn(None)
        when(webdriver_mock).find_element_by_name('q').thenReturn(mock_element)
        webdriverfactory_mock = mock(WebDriverFactory)
        when(webdriverfactory_mock).create_webdriver(testname=None).thenReturn(webdriver_mock)

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


    def test_newDriver_ReturnsNewInstance(self):
        config_reader = mock(ConfigReader)
        when(config_reader).get(WebDriverManager.SHUTDOWN_HOOK_CONFIG, True).thenReturn(True)
        when(config_reader).get(WebDriverManager.REUSE_BROWSER, True).thenReturn(False)
        when(config_reader).get(WebDriverManager.REUSE_BROWSER, True).thenReturn(False)

        webdriver_mock1 = mock(WebDriver)
        webdriver_mock2 = mock(WebDriver)
        webdriverfactory_mock = mock(WebDriverFactory)
        when(webdriverfactory_mock).create_webdriver(testname=None).thenReturn(webdriver_mock1).thenReturn(webdriver_mock2)
        
        webdriver_provider = WebDriverManager(webdriver_factory=webdriverfactory_mock, 
                                              config = config_reader)
        
        driver1 = webdriver_provider.new_driver()
        driver2 = webdriver_provider.new_driver()

        self.assertFalse(driver1 is driver2, 
                        "new_driver() should create fresh instance if reusebrowser if false.")

    @timeout(5)
    def test_multithreadMode(self):
        """
        Tests that when we call get_driver() it returns a unique driver for each thread,
        but for the same thread returns the same driver.
        """
        config_reader = mock(ConfigReader)
        when(config_reader).get(WebDriverManager.SHUTDOWN_HOOK_CONFIG, True).thenReturn(True)
        when(config_reader).get(WebDriverManager.REUSE_BROWSER, True).thenReturn(False)
        when(config_reader).get(WebDriverManager.REUSE_BROWSER, True).thenReturn(False)
        when(config_reader).get(WebDriverManager.ENABLE_THREADING_SUPPORT, False).thenReturn(True)
        
        webdriver_mock1 = mock(WebDriver)
        webdriver_mock2 = mock(WebDriver)
        webdriver_mock3 = mock(WebDriver)
        
        webdriverfactory_mock = mock(WebDriverFactory)
        when(webdriverfactory_mock).create_webdriver(testname=None).thenReturn(webdriver_mock1)\
        .thenReturn(webdriver_mock2).thenReturn(webdriver_mock3)

        webdriver_provider = WebDriverManager(webdriver_factory=webdriverfactory_mock, 
                                              config = config_reader)

        # Spawn thread to check if driver is unique per thread.
        driver1 = webdriver_provider.get_driver()
        t = threading.Thread(target=lambda: self.__multithreaded_7est_thread2(driver1, webdriver_provider))
        t.start()
        t.join()
        self.assertFalse(self._driver_from_thread_is_same)
        
        # Check that driver is same for the same thread.
        driver3 = webdriver_provider.get_driver()
        self.assertEqual(driver1, driver3, "Same thread should return same driver.")


    def __multithreaded_7est_thread2(self, driver1, webdriver_provider):
        # verify thread created
        driver2 =  webdriver_provider.get_driver()
        
        if driver1 == driver2:
            # This will cause the main thread to fail
            self._driver_from_thread_is_same = True
        else:
            self._driver_from_thread_is_same = False
             
        self.assertNotEqual(driver1, driver2, "Driver should be unique for each thread.")


    def test_cleanup_quits_webdrivers(self):
        "Tests that clean up is performed on webdrivers created by WebdriverManger"
        config_reader = mock(ConfigReader)
        when(config_reader).get(WebDriverManager.SHUTDOWN_HOOK_CONFIG, True).thenReturn(True)
        when(config_reader).get(WebDriverManager.REUSE_BROWSER, True).thenReturn(False)
        when(config_reader).get(WebDriverManager.REUSE_BROWSER, True).thenReturn(False)
        when(config_reader).get(WebDriverManager.ENABLE_THREADING_SUPPORT, False).thenReturn(True)
        
        webdriver_mock1 = mock(WebDriver)
        webdriverfactory_mock = mock(WebDriverFactory)
        when(webdriverfactory_mock).create_webdriver(testname=None).thenReturn(webdriver_mock1)

        webdriver_provider = WebDriverManager(webdriver_factory=webdriverfactory_mock, 
                                              config = config_reader)

        # Spawn thread to check if driver is unique per thread.
        driver = webdriver_provider.get_driver()
        del webdriver_provider
        
        # verify decontructor cleans up the webdriver.
        verify(driver).quit()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()