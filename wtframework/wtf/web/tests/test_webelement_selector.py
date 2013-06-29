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

from selenium.common.exceptions import ElementNotSelectableException
from selenium.webdriver.common.by import By
from wtframework.wtf.web.webelement import WebElementSelector, BadSelectorError
import unittest
from wtframework.wtf.web.webdriver import WTF_WEBDRIVER_MANAGER
from wtframework.wtf.utils.test_utils import do_and_ignore



class TestWebElementSelector(unittest.TestCase):
    '''
    Unit test of the PageObject Class
    '''

    driver = None
    
    def setUp(self):
        self.driver = WTF_WEBDRIVER_MANAGER.new_driver("TestWebElementSelector")
    
    def tearDown(self):
        do_and_ignore(lambda: WTF_WEBDRIVER_MANAGER.close_driver())

    def test_find_element_by_selectors_with_GoodSelectorFirst(self):
        self.driver.get("http://www.google.com")
        
        element = WebElementSelector.find_element_by_selectors(self.driver, 
                                                               (By.NAME, "q"))
        self.assertIsNotNone(element)
        


    def test_find_element_by_selectors_with_GoodSelector2nd(self):
        self.driver.get("http://www.google.com")
        
        element = WebElementSelector.find_element_by_selectors(self.driver, 
                                                               (By.NAME, "somenamenotingoogle.com.blah"),
                                                               (By.NAME, "q"))
        self.assertIsNotNone(element)


    def test_find_element_by_selectors_with_BadSelectors(self):
        self.driver.get("http://www.google.com")
        
        self.assertRaises(ElementNotSelectableException, \
                          WebElementSelector.find_element_by_selectors, \
                          self.driver, \
                          (By.NAME, "somenamenotingoogle.com.blah"), \
                          (By.ID, "anotherNotSlectable") \
        )


    def test_find_element_by_selectors_with_IncorrectSelectorTypes(self):
        self.driver.get("http://www.google.com")

        self.assertRaises(BadSelectorError, \
                          WebElementSelector.find_element_by_selectors, \
                          self.driver, \
                          (By.NAME, "somenamenotingoogle.com.blah"), \
                          ("not valid selector", "anotherNotSlectable") \
        )

