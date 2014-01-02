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
from mockito import mock, when
from nose.plugins.attrib import attr
from wtframework.wtf.config import ConfigReader, WTF_CONFIG_READER
from wtframework.wtf.web.webdriver import WebDriverFactory
import unittest2
import yaml
"""
NOTE:  These tests are all commented out.  These tests will not run over 
our Travis-CI/Sauce setup.  Ideally these tests should be ran manually 
before merging any code dealing with Webdriver Factory.
"""





class TestWebDriverFactory(unittest2.TestCase):
    '''
    Test the WebDriverFactory creates webdriver based on config.
    
    Note: most of these tests will be commented out because they many call physical browsers 
    or call external services that may bill us.
    '''


    def tearDown(self):
        #tear down any webdrivers we create.
        try:
            if self._driver: self._driver.close()
        except:
            pass
        self._driver = None




    #Tests running on local are skipped by default so the full suit can run on Travis-CI"
    @attr("noci")
    def test_createWebDriver_WithLocalBrowser(self):
        '''
        This will test this by opening firefox and trying to fetch Google with it.

        This test will normally be commented out since it spawns annoying browser windows.
        When making changes to WebDriverFactory, please run this test manually.
        '''
        config_reader = mock(ConfigReader)
        when(config_reader).get(WebDriverFactory.DRIVER_TYPE_CONFIG).thenReturn("LOCAL")
        when(config_reader).get(WebDriverFactory.BROWSER_TYPE_CONFIG).thenReturn("FIREFOX")

        driver_factory = WebDriverFactory(config_reader)
        self._driver = driver_factory.create_webdriver()
        
        # This whould open a local instance of Firefox.
        self._driver.get("http://www.google.com")
        
        # Check if we can use this instance of webdriver.
        self._driver.find_element_by_name('q') #google's famous q element.



    def test_createWebDriver_WithGrid(self):
        '''
        This will test a grid setup by making a connection to Sauce Labs.

        This test will normally be commented out since it will use billable automation hours 
        on sauce labs.
        '''
        config_reader = MockConfigWithSauceLabs()
        
        driver_factory = WebDriverFactory(config_reader)
        self._driver = driver_factory.create_webdriver("test_createWebDriver_WithGrid")
        exception = None
        try:
            self._driver.get('http://saucelabs.com/test/guinea-pig')
            self.assertGreater(self._driver.session_id, 0, "Did not get a return session id from Sauce.")
        except Exception as e:
            exception = e
        finally:
            # Make sure we quit sauce labs webdriver to avoid getting billed additonal hours.
            try:
                self._driver.quit()
            except:
                pass

        if exception != None:
            raise e


    def test_create_phantomjs_driver(self):
        config_reader = mock(ConfigReader)
        when(config_reader).get(WebDriverFactory.DRIVER_TYPE_CONFIG).thenReturn("LOCAL")
        when(config_reader).get(WebDriverFactory.BROWSER_TYPE_CONFIG).thenReturn("PHANTOMJS")
        
        try: # Check if the person running this test has a config specified for phantom JS, otherwise use default.
            path = WTF_CONFIG_READER.get(WebDriverFactory.PHANTOMEJS_EXEC_PATH)
            when(config_reader).get(WebDriverFactory.PHANTOMEJS_EXEC_PATH).thenReturn(path)
        except KeyError:
            when(config_reader).get(WebDriverFactory.PHANTOMEJS_EXEC_PATH).thenRaise(KeyError())

        driver_factory = WebDriverFactory(config_reader)
        self._driver = driver_factory.create_webdriver()

        # This whould open a local instance of Firefox.
        self._driver.get("http://www.google.com")

        # Check if we can use this instance of webdriver.
        self._driver.find_element_by_name('q') #google's famous q element.



class MockConfigWithSauceLabs(object):
    '''
    Mock config that returns sauce labs connection string.
    '''
    map = None
    
    def __init__(self):
        config = """
        selenium:
            type: REMOTE
            remote_url: {0}
            browser: FIREFOX
            desired_capabilities:
                platform: WINDOWS
                name: Unit Testing WD-acceptance-tests WebDriverFactory
        """.format(WTF_CONFIG_READER.get("selenium.remote_url"))
        # TODO: Might be good to replace this with a local grid to avoid using up SauceLab automation hours.
        self.map = yaml.load(config)



    def get(self,key, default_value=None):
        '''
        Gets the value from the yaml config based on the key.
        
        No type casting is performed, any type casting should be 
        performed by the caller.
        '''
        try:
            if "." in key:
                #this is a multi levl string
                namespaces = key.split(".")
                temp_var = self.map
                for name in namespaces:
                    temp_var = temp_var[name]
                return temp_var
            else:
                value = self.map[key]
                return value
        except:
            return default_value



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest2.main()

