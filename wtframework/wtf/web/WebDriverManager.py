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


    _singleton_instance = None #class variable to track singleton.
    webdriver = None #instance of webdriver.
    
    _webdriver_factory = None

    _mox = None

    def __init__(self, webdriver_factory=None):
        '''
        Initializer
        
        @param webdriver_factory: Optional webdriver factory to use to 
        create instances of webdriver.  This is useful for unit tests 
        that need to mock out the webdriver. 
        @type webdriver_factory: WebDriverFactory
        '''
        if( webdriver_factory != None):
            self._webdriver_factory = webdriver_factory
        else:
            self._webdriver_factory = WebDriverFactory()



    @staticmethod
    def get_instance():
        """
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its `__init__` method.
        On all subsequent calls, the already created instance is returned.
        
        @return: Singleton instance of WebDriverManager.
        @rtype: WebDriverManager
        """
        if WebDriverManager._singleton_instance == None:
            WebDriverManager._singleton_instance = WebDriverManager()

        return WebDriverManager._singleton_instance


    @staticmethod
    def clear_instance():
        '''
        Clear out the singleton instance.  This is useful for when you want to 
        reset the config settings and have it re-read in the settings.
        '''
        try:
            try:
                # If statement is to prevent instantiating a new webdriver in order to close it.
                if WebDriverManager._singleton_instance.webdriver != None:
                    WebDriverManager._singleton_instance.get_driver().close()
            except:
                pass
            WebDriverManager._singleton_instance = None
        except AttributeError:
            pass



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
WTF_WEBDRIVER_MANAGER = WebDriverManager.get_instance()