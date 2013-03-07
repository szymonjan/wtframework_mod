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
Created on Dec 17, 2012

@author: "David Lai"
'''
from wtframework.wtf.web.WebDriverFactory import WebDriverFactory


class WebDriverManager(object):
    '''
    Provides Singleton instance of Selenium WebDriver based on 
    config settings.
    
    Reason we don't make this a Utility class that provides a singleton 
    of the WebDriver itself is so we can allow that pice to be mocked 
    out to assist in unit testing framework classes that may use this. 
    '''


    def __init__(self, webdriver_factory=None):
        '''
        Initializer
        
        @param webdriver_factory: Optional webdriver factory to use to 
        create instances of webdriver.  This is useful for unit tests 
        that need to mock out the webdriver. 
        @type webdriver_factory: WebDriverFactory
        '''
        self.webdriver = None
        
        if( webdriver_factory != None):
            self._webdriver_factory = webdriver_factory
        else:
            self._webdriver_factory = WebDriverFactory()



    def get_driver(self):
        '''
        Get an instance of Selenium WebDriver.
        @return: Selenium WebDriver instance.
        @rtype: WebDriver
        '''
        if self.webdriver == None:
            self.webdriver = self._webdriver_factory.create_webdriver()

        return self.webdriver


    def is_driver_available(self):
        '''
        Check if a webdriver instance is created.
        @rtype: bool
        '''
        return self.webdriver != None


# Global Instance of WebDriver Manager
WTF_WEBDRIVER_MANAGER = WebDriverManager()