##########################################################################
# This file is part of WTFramework.
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
from mockito import mock, when
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from wtframework.wtf.config import ConfigReader
from wtframework.wtf.utils.test_utils import do_and_ignore
from wtframework.wtf.web.page import PageObject, InvalidPageError
from wtframework.wtf.web.webdriver import WTF_WEBDRIVER_MANAGER
import abc
import unittest2


class TestPageObject(unittest2.TestCase):

    '''
    Unit test of the PageObject Class
    '''

    driver = None

    def tearDown(self):
        do_and_ignore(lambda: WTF_WEBDRIVER_MANAGER.close_driver())

    def test_createPage_createsPageFromFactory(self):
        # Mock a webdriver that looks like it's viewing yahoo
        config_reader = mock()
        when(config_reader).get(
            "selenium.take_reference_screenshot", False).thenReturn(False)

        self.driver = WTF_WEBDRIVER_MANAGER.new_driver(
            "TestPageObject.test_createPage_createsPageFromFactory")
        self.driver.get("http://www.google.com")
        google = SearchPage.create_page(
            self.driver, config_reader=config_reader)
        self.assertTrue(type(google) == GoogleSearch)
        self.driver.get("http://www.yahoo.com")
        yahoo = SearchPage.create_page(
            self.driver, config_reader=config_reader)
        self.assertTrue(type(yahoo) == YahooSearch)

    def test_validatePage_GetsCalledDuringInit(self):
        '''
        Test the validate page and init elements is called when instantiating a page object.

        Note: This test is normally commented out since it launches webbrowsers.
        '''
        # Mock a webdriver that looks like it's viewing yahoo
        config_reader = mock(ConfigReader)
        when(config_reader).get(
            "selenium.take_reference_screenshot", False).thenReturn(False)
        driver = mock(WebDriver)
        when(driver).get("http://www.yahoo.com").thenReturn(None)
        when(driver).current_url = "http://www.yahoo.com"

        driver.get("http://www.yahoo.com")
        try:
            # Check we get an Invalid Page error.
            GoogleTestPageObj(driver, config_reader=config_reader)
            self.fail("Should of thrown exception.")
        except InvalidPageError:
            pass
        except Exception as e:
            self.fail(
                "Should throw an InvalidPageError, thrown was: " + str(type(e)))

        # Mock a WebDriver that looks like it's returning google.

        when(driver).get("http://www.google.com").thenReturn(None)
        driver.current_url = "http://www.google.com"
        element = mock(WebElement)
        # Create our 'q' element to test our init_Elements in PageObject.
        when(driver).find_element_by_name("q").thenReturn(element)

        # check if our Page object instantiates like normal
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


class SearchPage(PageObject):
    # abstract class.
    # needed to make this an abstract class in Python 2.7
    __metaclass__ = abc.ABCMeta


class GoogleSearch(SearchPage):

    def _validate_page(self, webdriver):
        if not "google.com" in webdriver.current_url:
            raise InvalidPageError("Not google.")


class YahooSearch(SearchPage):

    def _validate_page(self, webdriver):
        if not "yahoo.com" in webdriver.current_url:
            raise InvalidPageError("Not yahoo.")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest2.main()
