'''
Created on Dec 20, 2012

@author: "David Lai"
'''
from selenium import webdriver
from wtframework.wtf.config.ConfigReader import CONFIG_READER
from wtframework.wtf.web.WDDesiredCapabilities import \
    WDDesiredCapabilities
#import webdriverplus #Note: Pydev will display import error here, but this code should work.


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
            self._config_reader = CONFIG_READER

        try:
            if self._config_reader.get_value(WebDriverFactory.SHUTDOWN_HOOK_CONFIG) == True:
                WebDriverFactory._use_shutdown_hook = True
        except:
            pass

    @staticmethod
    def clean_up_webdrivers():
        '''
        Clean up webdrivers created during execution.
        '''
        # Quit webdrivers.
        try:
            if WebDriverFactory._use_shutdown_hook:
                for webdriver in WebDriverFactory._webdrivers_created:
                    try:
                        webdriver.quit()
                    except:
                        pass
        except:
            pass


    def create_webdriver(self):
        '''
            Creates an instance of Selenium webdriver based on config settings.
            This should only be called by a shutdown hook.  Do not call directly within 
            a test.

            @return: WebDriver
        '''
        driver_type = self._config_reader.get_value(WebDriverFactory.DRIVER_TYPE_CONFIG)

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
        browser_type = self._config_reader.get_value(WebDriverFactory.BROWSER_TYPE_CONFIG)

        browser_type_dict = {\
                             self.CHROME: lambda:webdriver.Chrome(self._config_reader.get_value(WebDriverFactory.CHROME_DRIVER_PATH)),\
                             self.FIREFOX: lambda:webdriver.Firefox(),\
                             self.INTERNETEXPLORER: lambda:webdriver.Ie(),\
                             self.OPERA:lambda:webdriver.Opera()}
        # Currently not supporting HTML unit driver due to JS issues that prevent it from 
        # working with our site.
        # "HTMLUNIT": lambda: self.__create_html_unit_driver()}
        try:
            return browser_type_dict[browser_type]()
        except KeyError:
            raise TypeError("Unsupported Browser Type {0}".format(browser_type))        
        # End of method.

    def __create_remote_webdriver_from_config(self):
        '''
        Reads the config value for browser type.
        '''
        browser_type = self._config_reader.get_value(WebDriverFactory.BROWSER_TYPE_CONFIG)
        remote_url = self._config_reader.get_value(WebDriverFactory.REMOTE_URL_CONFIG)

        browser_constant_dict = {self.HTMLUNIT:WDDesiredCapabilities.HTMLUNIT, \
                                 self.HTMLUNITWITHJS:WDDesiredCapabilities.HTMLUNITWITHJS, \
                                 self.ANDROID:WDDesiredCapabilities.ANDROID,\
                                 self.CHROME:WDDesiredCapabilities.CHROME,\
                                 self.FIREFOX:WDDesiredCapabilities.FIREFOX,\
                                 self.INTERNETEXPLORER:WDDesiredCapabilities.INTERNETEXPLORER,\
                                 self.IPAD:WDDesiredCapabilities.IPAD,\
                                 self.IPHONE:WDDesiredCapabilities.IPHONE,\
                                 self.OPERA:WDDesiredCapabilities.OPERA }
        # Currently not supporting safari due to issues with the safari webdriver.
        # "SAFARI":WDDesiredCapabilities.SAFARI}
        
        try:
            desired_capabilities = browser_constant_dict[browser_type]
        except KeyError:
            raise TypeError("Unsupported Browser Type {0}".format(browser_type))

        # Get additional desired properties from config file and add them in.
        other_desired_capabilities = self._config_reader.get_value(WebDriverFactory.DESIRED_CAPABILITIES_CONFIG)

        for prop in other_desired_capabilities:
            value = other_desired_capabilities[prop]
            if isinstance(value, basestring):
                desired_capabilities[prop] = value
            else:
                desired_capabilities[prop] = str(value)

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
