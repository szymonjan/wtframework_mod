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
'''
Created on Jan 29, 2013

@author: "David Lai"
'''
from selenium import webdriver
from wtframework.wtf.web.PageFactory import PageFactory, \
    NoMatchingPageError
from wtframework.wtf.web.PageObject import PageObject, \
    InvalidPageError
import abc
import unittest



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
        try:
            self.driver.close()
        except:
            pass
        

    @unittest.skip("This test relies on a browser and internet connection.")
    def test_createPage_createsPageWhenExists(self):
        self.driver = webdriver.Firefox()
        self.driver.get("http://www.google.com")
        google = PageFactory.create_page(self.driver, PageObject)
        self.assertTrue(type(google) == GoogleSearch)
        self.driver.get("http://www.yahoo.com")
        yahoo = PageFactory.create_page(self.driver, PageObject)
        self.assertTrue(type(yahoo) == YahooSearch)

    @unittest.skip("This test relies on a browser and internet connection.")
    def test_createPage_raiseExceptionWhenNoMatch(self):
        self.driver = webdriver.Firefox()
        self.driver.get("http://www.amazon.com")
        self.assertRaises(NoMatchingPageError, PageFactory.create_page, self.driver, SearchPage)



class SearchPage(PageObject):
    #abstract class.
    __metaclass__ = abc.ABCMeta #needed to make this an abstract class in Python 2.7

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
    unittest.main()
    
    