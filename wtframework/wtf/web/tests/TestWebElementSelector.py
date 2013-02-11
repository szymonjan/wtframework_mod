'''
Created on Feb 6, 2013

@author: "David Lai"
'''

from selenium.common.exceptions import ElementNotSelectableException
from selenium.webdriver.common.by import By
from wtframework.wtf.web.WebDriverManager import WTF_WEBDRIVER_MANAGER
from wtframework.wtf.web.WebElementSelector import WebElementSelector, \
    BadSelectorError
import unittest


'''
Created on Dec 21, 2012

@author: "David Lai"
'''


class TestWebElementSelector(unittest.TestCase):
    '''
    Unit test of the PageObject Class
    '''

    driver = None
    
    def setUp(self):
        self.driver = WTF_WEBDRIVER_MANAGER.get_driver()
    
    def tearDown(self):
        try:
            self.driver.close()
        except:
            pass
        

    @unittest.skip("This test relies on a browser and internet connection.")
    def test_find_element_by_selectors_with_GoodSelectorFirst(self):
        self.driver.get("http://www.google.com")
        
        element = WebElementSelector.find_element_by_selectors(self.driver, 
                                                               (By.NAME, "q"))
        self.assertIsNotNone(element)
        

    @unittest.skip("This test relies on a browser and internet connection.")
    def test_find_element_by_selectors_with_GoodSelector2nd(self):
        self.driver.get("http://www.google.com")
        
        element = WebElementSelector.find_element_by_selectors(self.driver, 
                                                               (By.NAME, "somenamenotingoogle.com.blah"),
                                                               (By.NAME, "q"))
        self.assertIsNotNone(element)

    @unittest.skip("This test relies on a browser and internet connection.")
    def test_find_element_by_selectors_with_BadSelectors(self):
        self.driver.get("http://www.google.com")
        
        self.assertRaises(ElementNotSelectableException, \
                          WebElementSelector.find_element_by_selectors, \
                          self.driver, \
                          (By.NAME, "somenamenotingoogle.com.blah"), \
                          (By.ID, "anotherNotSlectable") \
        )

    @unittest.skip("This test relies on a browser and internet connection.")
    def test_find_element_by_selectors_with_IncorrectSelectorTypes(self):
        self.driver.get("http://www.google.com")

        self.assertRaises(BadSelectorError, \
                          WebElementSelector.find_element_by_selectors, \
                          self.driver, \
                          (By.NAME, "somenamenotingoogle.com.blah"), \
                          ("not valid selector", "anotherNotSlectable") \
        )

