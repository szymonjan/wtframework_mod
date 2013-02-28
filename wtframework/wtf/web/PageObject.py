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
Created on Dec 21, 2012

@author: "David Lai"
'''
from wtframework.wtf.config.ConfigReader import WTF_CONFIG_READER
from wtframework.wtf.web.WebScreenshotUtil import WebScreenShotUtil
import abc


class PageObject(object):
    '''
    Baseclass for PageObjects.
    
    Basic Usage:
    1) define 'validate_page' method.  This method will check to make sure 
       we are on the correct page.
    2) define 'get_element_locators' method.  This will fetch a list of locators that'll 
       be used to initialize elements.
    '''
    __metaclass__ = abc.ABCMeta #needed to make this an abstract class in Python 2.7

    # Webdriver associated with this instance of the PageObject

    _names_of_classes_we_already_took_screen_caps_of = {}

    def __init__(self, webdriver, config_reader = WTF_CONFIG_READER):
        '''
        Constructor
        @param webdriver: WebDriver
        @type webdriver: WebDriver
        '''
        self._validate_page(webdriver)

        self.webdriver = webdriver

        # Take reference screenshots if this option is enabled.
        if config_reader.get_value("selenium.take_reference_screenshot") == True:
            class_name = type(self).__name__
            if class_name in PageObject._names_of_classes_we_already_took_screen_caps_of:
                pass
            else:
                try:
                    WebScreenShotUtil.take_reference_screenshot(webdriver, class_name)
                    PageObject._names_of_classes_we_already_took_screen_caps_of[class_name] = True
                except Exception as e:
                    print e # Some WebDrivers such as headless drivers does not take screenshots.

        else:
            pass


    @abc.abstractmethod
    def _validate_page(self, webdriver):
        """
        Perform checks to validate this page is the correct target page.
        
        @raise IncorrectPageException: Raised when we try to assign the wrong page 
        to this page object.
        """
        return


    @classmethod
    def create_page(cls, webdriver, config_reader = WTF_CONFIG_READER):
        """
        Class method short cut to call PageFactory on itself.
        @param webdriver: WebDriver to associate with this page.
        @type webdriver: WebDriver
        """
        # Note, the delayed import here is to avoid a circular import.
        from wtframework.wtf.web.PageFactory import PageFactory
        return PageFactory.create_page(webdriver, cls, config_reader=config_reader)


    #Magic methods for enabling comparisons.
    def __cmp__(self, other):
        """
        Override this to implement PageObject ranking.  This is used by PageObjectFactory
        when it finds multiple pages that qualify to map to the current page.  The 
        PageObjectFactory will check which page object is preferable.
        """
        return 0


class InvalidPageError(Exception):
    '''Thrown when we have tried to instantiate the incorrect page to a PageObject.'''