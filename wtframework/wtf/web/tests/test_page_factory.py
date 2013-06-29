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
from wtframework.wtf.web.page import NoMatchingPageError, InvalidPageError, \
    PageFactory, PageObject
from wtframework.wtf.web.webdriver import WTF_WEBDRIVER_MANAGER
import abc
import unittest
from wtframework.wtf.utils.test_utils import do_and_ignore

# Interface for the other 2 search pages to implement.
class SearchPage(PageObject):
    #abstract class.
    __metaclass__ = abc.ABCMeta #needed to make this an abstract class in Python 2.7

class GoogleSearch(SearchPage):
    
    def _validate_page(self, webdriver):
        if not "google.com" in webdriver.current_url:
            raise InvalidPageError("Not google.")

    def __cmp__(self, other):
        return 0


class YahooSearch(SearchPage):
    
    def _validate_page(self, webdriver):
        if not "yahoo.com" in webdriver.current_url:
            raise InvalidPageError("Not yahoo.")


class GoogleSearch2(PageObject):
    
    def _validate_page(self, webdriver):
        if not "google.com" in webdriver.current_url:
            raise InvalidPageError("Not google.")
    def __cmp__(self, other):
        return 1;




class TestPageFactory(unittest.TestCase):
    '''
    Test the WebDriverFactory creates webdriver based on config.
    
    Note: most of these tests will be commented out because they many call physical browsers 
    or call external services that may bill us.
    '''

    driver = None


    def tearDown(self):
        self._mocker = None
        #tear down any webdrivers we create.
        do_and_ignore(lambda: WTF_WEBDRIVER_MANAGER.close_driver())


    def test_create_page_createsPageWhenExists(self):
        self.driver = WTF_WEBDRIVER_MANAGER.new_driver("TestPageFactor.test_create_page_createsPageWhenExists")
        self.driver.get("http://www.google.com")
        google = PageFactory.create_page(SearchPage, self.driver)
        self.assertTrue(type(google) == GoogleSearch)
        self.driver.get("http://www.yahoo.com")
        yahoo = PageFactory.create_page(SearchPage, self.driver)
        self.assertTrue(type(yahoo) == YahooSearch)


    def test_create_page_raiseExceptionWhenNoMatch(self):
        self.driver = WTF_WEBDRIVER_MANAGER.new_driver("TestPageFactor.test_create_page_raiseExceptionWhenNoMatch")
        self.driver.get("http://www.amazon.com")
        self.assertRaises(NoMatchingPageError, PageFactory.create_page, SearchPage, self.driver)


    def test_create_page_with_list(self):
        self.driver = WTF_WEBDRIVER_MANAGER.new_driver("TestPageFactor.test_create_page_with_list")
        self.driver.get("http://www.google.com")
        google = PageFactory.create_page([GoogleSearch, YahooSearch], self.driver)
        self.assertTrue(type(google) == GoogleSearch)
        self.driver.get("http://www.yahoo.com")
        yahoo = PageFactory.create_page([GoogleSearch, YahooSearch], self.driver)
        self.assertTrue(type(yahoo) == YahooSearch)

    def test_create_page_uses_page_rank(self):
        self.driver = WTF_WEBDRIVER_MANAGER.new_driver("TestPageFactor.test_create_page_uses_page_rank")
        self.driver.get("http://www.google.com")
        google_page = PageFactory.create_page([GoogleSearch, GoogleSearch2], self.driver)
        self.assertTrue(isinstance(google_page, GoogleSearch2))



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    