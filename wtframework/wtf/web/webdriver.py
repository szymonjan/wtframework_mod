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

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from wtframework.wtf.config import WTF_CONFIG_READER



class WebDriverFactory(object):
    '''
    This class constructs a Selenium Webdriver using settings in the config file.
    
    Note: please be sure to uncomment the Unit test and run them manually before 
    pushing any changes.  This is because they are disabled.  The reason is 
    because the unit tests for this class can use up billable hours on sauce labs 
    or open annoying browser windows.
    '''

    # CONFIG SETTINGS #
    DRIVER_TYPE_CONFIG = "selenium.type"
    REMOTE_URL_CONFIG = "selenium.remote_url"
    BROWSER_TYPE_CONFIG = "selenium.browser"
    DESIRED_CAPABILITIES_CONFIG = "selenium.desired_capabilities"
    SHUTDOWN_HOOK_CONFIG = "selenium.shutdown_hook"
    CHROME_DRIVER_PATH = "selenium.chromedriver_path"

    _DEFAULT_SELENIUM_SERVER_FOLDER = "selenium-server"

    # BROWSER CONSTANTS #
    HTMLUNIT = "HTMLUNIT"
    HTMLUNITWITHJS = "HTMLUNITWITHJS"
    ANDROID = "ANDROID"
    CHROME = "CHROME"
    FIREFOX = "FIREFOX"
    INTERNETEXPLORER = "INTERNETEXPLORER"
    IPAD = "IPAD"
    IPHONE = "IPHONE"
    OPERA = "OPERA"
    PHANTOMJS = "PHANTOMJS"
    SAFARI = "SAFARI"


    # Instance Variables#
    _config_reader = None
    _use_shutdown_hook = False
    _webdrivers_created = []

    def __init__(self, config_reader=None):
        '''
        Initializer.
        
        @param config_reader: Pass in a config reader if you want to stub this out.
        @type config_reader: ConfigReader
        '''

        if config_reader != None:
            self._config_reader = config_reader
        else:
            self._config_reader = WTF_CONFIG_READER

        if self._config_reader.get(WebDriverFactory.SHUTDOWN_HOOK_CONFIG, True) == True:
            WebDriverFactory._use_shutdown_hook = True
        else:
            WebDriverFactory._use_shutdown_hook = False
        

    @staticmethod
    def clean_up_webdrivers():
        '''
        Clean up webdrivers created during execution.
        '''
        # Quit webdrivers.
        print "Cleaning up webdrivers"
        try:
            if WebDriverFactory._use_shutdown_hook:
                for webdriver in WebDriverFactory._webdrivers_created:
                    try:
                        webdriver.quit()
                    except Exception as e:
                        print e
        except:
            pass


    def create_webdriver(self):
        '''
            Creates an instance of Selenium webdriver based on config settings.
            This should only be called by a shutdown hook.  Do not call directly within 
            a test.

            @return: WebDriver
        '''
        try:
            driver_type = self._config_reader.get(WebDriverFactory.DRIVER_TYPE_CONFIG)
        except:
            print WebDriverFactory.DRIVER_TYPE_CONFIG + " setting is missing from config. Using defaults"
            driver_type = "LOCAL"

        if driver_type == "REMOTE":
            # Create desired capabilities.
            self.webdriver = self.__create_remote_webdriver_from_config()
        else:
            #handle as local webdriver
            self.webdriver = self.__create_driver_from_browser_config()

        #add webdriver to list of drivers to be cleaned up.
        WebDriverFactory._webdrivers_created.append(self.webdriver)

        self.webdriver.maximize_window()

        return self.webdriver
        
    def __create_driver_from_browser_config(self):
        '''
        Reads the config value for browser type.
        '''
        try:
            browser_type = self._config_reader.get(WebDriverFactory.BROWSER_TYPE_CONFIG)
        except KeyError:
            print WebDriverFactory.BROWSER_TYPE_CONFIG + " missing is missing from config file. Using defaults"
            browser_type = WebDriverFactory.FIREFOX

        browser_type_dict = {\
                             WebDriverFactory.CHROME: lambda:webdriver.Chrome(self._config_reader.get(WebDriverFactory.CHROME_DRIVER_PATH)),\
                             WebDriverFactory.FIREFOX: lambda:webdriver.Firefox(),\
                             WebDriverFactory.INTERNETEXPLORER: lambda:webdriver.Ie(),\
                             WebDriverFactory.OPERA:lambda:webdriver.Opera(),
                             WebDriverFactory.PHANTOMJS:lambda:webdriver.PhantomJS()}

        try:
            return browser_type_dict[browser_type]()
        except KeyError:
            raise TypeError("Unsupported Browser Type {0}".format(browser_type))        
        # End of method.

    def __create_remote_webdriver_from_config(self):
        '''
        Reads the config value for browser type.
        '''
        browser_type = self._config_reader.get(WebDriverFactory.BROWSER_TYPE_CONFIG)
        remote_url = self._config_reader.get(WebDriverFactory.REMOTE_URL_CONFIG)

        browser_constant_dict = {WebDriverFactory.HTMLUNIT:DesiredCapabilities.HTMLUNIT, \
                                 WebDriverFactory.HTMLUNITWITHJS:DesiredCapabilities.HTMLUNITWITHJS, \
                                 WebDriverFactory.ANDROID:DesiredCapabilities.ANDROID,\
                                 WebDriverFactory.CHROME:DesiredCapabilities.CHROME,\
                                 WebDriverFactory.FIREFOX:DesiredCapabilities.FIREFOX,\
                                 WebDriverFactory.INTERNETEXPLORER:DesiredCapabilities.INTERNETEXPLORER,\
                                 WebDriverFactory.IPAD:DesiredCapabilities.IPAD,\
                                 WebDriverFactory.IPHONE:DesiredCapabilities.IPHONE,\
                                 WebDriverFactory.OPERA:DesiredCapabilities.OPERA ,\
                                 WebDriverFactory.SAFARI:DesiredCapabilities.SAFARI,
                                 WebDriverFactory.PHANTOMJS:DesiredCapabilities.PHANTOMJS}
        
        try:
            desired_capabilities = browser_constant_dict[browser_type]
        except KeyError:
            raise TypeError("Unsupported Browser Type {0}".format(browser_type))

        # Get additional desired properties from config file and add them in.
        other_desired_capabilities = self._config_reader.get(WebDriverFactory.DESIRED_CAPABILITIES_CONFIG)

        for prop in other_desired_capabilities:
            value = other_desired_capabilities[prop]
            if isinstance(value, basestring):
                desired_capabilities[prop] = value
            else:
                desired_capabilities[prop] = str(value)

        # Set the test name property if specified in the WTF_TESTNAME var.
        try:
            test_name = self._config_reader.get("TESTNAME")
            desired_capabilities['name'] = test_name
        except KeyError:
            pass # No test name is specified, use the default.

        # Instantiate remote webdriver.
        return webdriver.Remote(
            desired_capabilities = desired_capabilities,
            command_executor = remote_url
        )
        # End of method.

# NOTE: HTML Unit driver is only available on Java at this time. 1/31/13
#    def __create_html_unit_driver(self):
#        "Create a HTML unit driver by spawning a selenium server process."
#        # Note: We are using webdriverplus here.  This 3rd party lib will perform 
#        # the process of wrapping up a selenium server and exposing it to us as a 
#        # web driver.  Keep in mind though, this webdriver may not have the same 
#        # level of functionality as the other webdrivers.
#        driver = webdriverplus.WebDriver('htmlunit')
#        return driver


# End of Class.

# Adding a shut down hook for cleaning up webdrivers that get 
# created by WebDriverFactory.
try: 
    import atexit
    atexit.register(WebDriverFactory.clean_up_webdrivers)
except:
    pass




class WebDriverManager(object):
    '''
    Provides Singleton instance of Selenium WebDriver based on 
    config settings.
    
    Reason we don't make this a Utility class that provides a singleton 
    of the WebDriver itself is so we can allow that pice to be mocked 
    out to assist in unit testing framework classes that may use this. 
    '''
    REUSE_BROWSER = "selenium.reusebrowser"


    def __init__(self, webdriver_factory=None, config=WTF_CONFIG_READER):
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

        self.__config = WTF_CONFIG_READER


    def new_driver(self):
        '''
        Used at a start of a test to get a new instance of webdriver.  If the 
        'resuebrowser' setting is true, it will use a recycled webdriver instance.
        @return: Selenium WebDriver instance.
        @rtype: WebDriver
        '''
        if self.__config.get(WebDriverManager.REUSE_BROWSER, True):
            if self.webdriver == None:
                self.webdriver = self._webdriver_factory.create_webdriver()
            else:
                try:
                    # Clear cookies and check if webdriver is still healthy.
                    self.webdriver.delete_all_cookies()
                    self.webdriver.get("about:blank") #check to see if webdriver is still responding
                except:
                    try:
                        self.webdriver.quit()
                    except:
                        pass
                    self.webdriver = self._webdriver_factory.create_webdriver()
                
        else:
            # Attempt to tear down any existing webdriver.
            if self.webdriver is not None:
                try:
                    self.webdriver.quit()
                except:
                    pass
                
                self.webdriver = self._webdriver_factory.create_webdriver()


        return self.webdriver


    def get_driver(self):
        '''
        Get an already running instance of webdriver. If there is none, it will create one.
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



