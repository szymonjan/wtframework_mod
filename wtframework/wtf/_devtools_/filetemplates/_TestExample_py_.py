content = \
'''
"""
EXAMPLE TEST
Created on Feb 6, 2013

@author: davidlai
"""
import unittest
from wtframework.wtf.wdtestobjects.WTFBaseTest import WTFBaseTest
from wtframework.wtf.web.WebDriverManager import WTF_WEBDRIVER_MANAGER
from wtframework.wtf.web.PageFactory import PageFactory
from tests.pages.GoogleSearchPage import GoogleSearchPage
from tests.pages.ISearchPage import ISearchPage
from tests.pages.YahooSearchPage import YahooSearchPage

# Extend the WTFBaseTest to get access to WTF added features like 
# taking screenshot on test failure.
class Test(WTFBaseTest):


    def test_basic_example(self):
        "Displays a simple PageObject instantiation example."
        
        # WTF_WEBDRIVER_MANAGER provides a easy to access singleton to 
        # access the webdriver.  A web browser will be instantiated 
        # according to your config settings. 
        # - see 'selenium' settings in 'configs/default.yaml'
        webdriver = WTF_WEBDRIVER_MANAGER.get_driver()
        webdriver.get("http://www.google.com")
        
        # Use the PageFactory class to instantiate your page.
        google_page = PageFactory.create_page(webdriver, GoogleSearchPage)
        
        # With your PageObject instantiated, you can call it's methods.
        google_page.search("hello world")
        self.assertTrue(google_page.result_contains("hello world"))



    def test_example_using_abstract_interfaces(self):
        "Demonstrates creating PageObjects using Abstract Factory pattern."
        webdriver = WTF_WEBDRIVER_MANAGER.get_driver()
        webdriver.get("http://www.google.com")
        
        # Notice I don't need specify GoogleSearchPage specifically, and
        # able to construct a ISearchPage of the correct type.
        search_page = PageFactory.create_page(webdriver, ISearchPage)
        self.assertEqual(GoogleSearchPage, type(search_page))
        
        webdriver.get("http://www.yahoo.com")
        search_page = PageFactory.create_page(webdriver, ISearchPage)
        self.assertEqual(YahooSearchPage, type(search_page))



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
'''