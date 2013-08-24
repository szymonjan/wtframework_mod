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
from datetime import datetime, timedelta
from selenium.common.exceptions import ElementNotSelectableException, \
    TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from wtframework.wtf.config import WTF_TIMEOUT_MANAGER
import time


class WebElementSelector():
    "Utiltiy class for selecting elements."


    @staticmethod
    def find_element_by_selectors(webdriver, *selectors):
        """
        Utility method makes it easier to find an element using multiple selectors. This is 
        useful for problematic elements what might works with one browser, but fail in another.
        
        Args:
            selectors - var arg if N number of selectors to match against.  Each selector should 
                        be a Selenium 'By' object.
        
        Usage::
            my_element = WebElementSelector.find_element_by_selectors(webdriver,
                                                                    (By.ID, "MyElementID"),
                                                                    (By.CSS, "MyClassSelector") )


        """
        #perform initial check to verify selectors are valid by statements.
        for selector in selectors:
            (by_method, value) = selector
            if not WebElementSelector.__is_valid_by_type(by_method):
                raise BadSelectorError("Selectors should be of type selenium.webdriver.common.by.By")
            if type(value) != str:
                raise BadSelectorError("Selectors should be of type selenium.webdriver.common.by.By")
        
        selectors_used = []
        for selector in selectors:
            (by_method, value) = selector
            selectors_used.append("{by}:{value}".format(by=by_method, value=value))
            try:
                return webdriver.find_element(by=by_method, value=value)
            except:
                pass
        
        raise ElementNotSelectableException("Unable to find elements using:" + ",".join(selectors_used))

    @staticmethod
    def __is_valid_by_type(by_type):
        for attr, value in By.__dict__.iteritems():
            if "__" not in attr:
                if by_type == value:
                    return True
        
        return False
    

class WebElementUtils():    
    """
    Utility methods for working with web pages and web elements.
    """


    @staticmethod
    def wait_until_element_not_visible(webdriver, locator_lambda_expression, \
                                       timeout=WTF_TIMEOUT_MANAGER.NORMAL, sleep=0.5):
        """
        Wait for a WebElement to disappear.
        
        Args:
            webdriver (Webdriver) - Selenium Webdriver
            locator (lambda) - Locator lambda expression.

        Kwargs:
            timeout (number) - timeout period
            sleep (number) - sleep period between intervals.

        """
        # Wait for loading progress indicator to go away.
        try:
            stoptime = datetime.now() + timedelta(seconds=timeout)
            while datetime.now() < stoptime:
                element = WebDriverWait(webdriver, WTF_TIMEOUT_MANAGER.BRIEF).until(locator_lambda_expression)
                if element.is_displayed():
                    time.sleep(sleep)
                else:
                    break
        except TimeoutException:
            pass


    @staticmethod
    def is_image_loaded(webdriver, webelement):
        '''
        Check if an image (in an image tag) is loaded.
        Note: This call will not work against background images.  Only Images in <img> tags.

        Args:
            webelement (WebElement) - WebDriver web element to validate.

        '''
        script = "return arguments[0].complete && type of arguments[0].naturalWidth != \"undefined\" " +\
                 "&& arguments[0].naturalWidth > 0"
        try:
            return webdriver.execute_script(script, webelement)
        except:
            return False #Img Tag Element is not on page.


class BadSelectorError(Exception):
    "Raised when a bad selector is passed into a WebElementSelector() method."
    pass

