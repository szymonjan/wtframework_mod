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

