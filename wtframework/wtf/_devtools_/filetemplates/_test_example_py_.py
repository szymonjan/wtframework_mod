content = \
'''
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


from tests.pages.search_page import ISearchPage
from tests.pages.www_google_com import GoogleSearchPage
from tests.pages.www_yahoo_com import YahooSearchPage
from wtframework.wtf.testobjects.basetests import WTFBaseTest
from wtframework.wtf.web.page import PageFactory
from wtframework.wtf.web.webdriver import WTF_WEBDRIVER_MANAGER
import time
import unittest

# Extend the WTFBaseTest to get access to WTF added features like 
# taking screenshot on test failure.
class Test(WTFBaseTest):


    def test_basic_example(self):
        "Displays a simple PageObject instantiation example."
        
        # WTF_WEBDRIVER_MANAGER provides a easy to access singleton to 
        # access the webdriver.  A web browser will be instantiated 
        # according to your config settings. 
        # - see 'selenium' settings in 'configs/default.yaml'
        webdriver = WTF_WEBDRIVER_MANAGER.new_driver()
        webdriver.get("http://www.google.com")
        
        # Use the PageFactory class to instantiate your page.
        google_page = PageFactory.create_page(GoogleSearchPage, webdriver)
        
        # With your PageObject instantiated, you can call it's methods.
        google_page.search("hello world")
        time.sleep(5)
        self.assertTrue(google_page.result_contains("hello world"))



    def test_example_using_abstract_interfaces(self):
        "Demonstrates creating PageObjects using Abstract Factory pattern."
        webdriver = WTF_WEBDRIVER_MANAGER.new_driver()
        webdriver.get("http://www.google.com")

        
        # Notice I don't need specify GoogleSearchPage specifically, and
        # able to construct a ISearchPage of the correct type.
        search_page = PageFactory.create_page(ISearchPage, webdriver)
        self.assertEqual(GoogleSearchPage, type(search_page))
        
        webdriver.get("http://www.yahoo.com")
        search_page = PageFactory.create_page(ISearchPage, webdriver)
        self.assertEqual(YahooSearchPage, type(search_page))



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
'''