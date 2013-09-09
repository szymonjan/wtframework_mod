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
examples = {}

examples['tests/__init__.py'] = '''
'''

examples['tests/flows/__init__.py'] = '''
'''

examples['tests/flows/search_flows.py'] = '''##########################################################################
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

from tests.pages.search_page import ISearchPage
from wtframework.wtf.config import WTF_TIMEOUT_MANAGER
from wtframework.wtf.web.page import PageFactory


# You can use flow functions to group together a set of calls you make frequently 
# so you can reuse them between tests.

def perform_search(search_term, webdriver):
    """
    This flow function groups together a navigation to the search page, and 
    a search.
    """
    webdriver.get("http://www.google.com")
    search_page = PageFactory.create_page(ISearchPage, webdriver)
    search_page.search(search_term)
    WTF_TIMEOUT_MANAGER.brief_pause() #brief pause to allow type-ahead search to trigger.
    return search_page
'''

examples['tests/models/__init__.py'] = '''
'''

examples['tests/pages/__init__.py'] = '''# Import your subpages Implementing an Interface in the 
# "__init__.py" so PageFactory will no about it's existence.
from tests.pages.www_google_com import GoogleSearchPage #@UnusedImport
from tests.pages.www_yahoo_com import YahooSearchPage #@UnusedImport

'''

examples['tests/pages/search_page.py'] = '''
import abc


class ISearchPage(object):
    """
    Example of how you can use a mix-in as an interface.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def search(self, search_string):
        "Submit a search"
        pass
    
    @abc.abstractmethod
    def result_contains(self):
        "Submit a search"
        pass
'''

examples['tests/pages/www_google_com.py'] = '''
from tests.pages.search_page import ISearchPage
from wtframework.wtf.web.page import PageObject, InvalidPageError



# Extend PageObject to create a page object.  You can also use Mix-Ins 
# to implement interfaces to use with PageFactory.
class GoogleSearchPage(PageObject, ISearchPage):
    """
    Example Page Object Using Google.
    """
    
    # Object Mappings for fields on this page. #
    # Note the 'self.webdriver', this is because PageObjects keep track 
    # of their own webdriver that's driving the page.
    search_field = lambda self:self.webdriver.find_element_by_name('q')
    
    # Page objects all override the _validate_page() method so pages 
    # can self validate upon creation.
    def _validate_page(self, webdriver):
        "Check to make sure we're on google.com"
        if "google.com" not in webdriver.current_url:
            # Raise an InvalidPageError to let the PageFactory 
            # know that this isn't a page match.
            raise InvalidPageError("This is not google.")

    
    # Here we are implementing the Search method as defined by 
    # ISearchPage interface.
    def search(self, search_string):
        "Enter a search"
        
        # We can call a mapped element by calling it's lambda function.
        self.search_field().send_keys(search_string)
        

    # Here we are implementing the validate result contains method.
    def result_contains(self, text_to_check):
        "Simple check to see if the word occurs in the page."
        return text_to_check in self.webdriver.page_source
        
'''

examples['tests/pages/www_yahoo_com.py'] = '''

from wtframework.wtf.web.page import PageObject, InvalidPageError
from tests.pages.search_page import ISearchPage

class YahooSearchPage(PageObject, ISearchPage):
    "Simple PageObject class"
    
    # Object Mappings for fields on this page. #
    # Note the 'self.webdriver', this is because PageObjects keep track 
    # of their own webdriver that's driving the page.
    search_field = lambda self:self.webdriver.find_element_by_name('p')
    submit_button = lambda self:self.webdriver.find_eleent_by_id('search-submit')
    
    # Page objects all override the _validate_page() method so pages 
    # can self validate upon creation.
    def _validate_page(self, webdriver):
        "Check to make sure we're on google.com"
        if "yahoo.com" not in webdriver.current_url:
            # Raise an InvalidPageError to let the PageFactory 
            # know that this isn't a page match.
            raise InvalidPageError("This is not Yahoo.")

    
    # Here we are implementing the Search method as defined by 
    # ISearchPage interface.
    def search(self, search_string):
        "Enter a search"
        
        # We can call a mapped element by calling it's lambda function.
        self.search_field().send_keys(search_string)
        self.submit_button().submit_button
        

    # Here we are implementing the validate result contains method.
    def result_contains(self, text_to_check):
        "Simple check to see if the word occurs in the page."
        return text_to_check in self.webdriver.page_source
        
'''

examples['tests/support/__init__.py'] = '''
'''

examples['tests/testdata/__init__.py'] = '''
'''

examples['tests/testdata/settings.py'] = '''##########################################################################
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
from wtframework.wtf.config import WTF_CONFIG_READER

# The idea of a 'testdata' package is to organize your test data and test settings.
# While tests can reference the WTF_CONFIG_READER directly like this
#
#    admin_user = WTF_CONFIG_READER.get("admin_user", "admin")
#
# But you'll have the same hard coded "admin_user" string all over your tests.
# It is better to abstract that away into function calls so the same hard coded 
# string isn't repeated throughout your code.  This creates a single point of 
# maintenance for any config refactoring.
#
#
# This is an example of how you can uses a settings object.
# Here in your test, you can now refer to your admin login 
# like this
#
#     login_page.login( get_admin_user(), get_test_admin_password() )
#
# Then when you run on different envionrments or different accounts,
# you can simply pass in a config file that'll specify the value for 
# 'admin_user' and 'admin_password'
def get_admin_user():
    return WTF_CONFIG_READER.get("admin_user", "admin")

def get_admin_password():
    return WTF_CONFIG_READER.get("admin_password", "password")
'''

examples['tests/tests/__init__.py'] = '''# Import your subpages Implementing an Interface in the 
# "__init__.py" so PageFactory will no about it's existence.
import tests.pages.www_google_com #@UnusedImport
import tests.pages.www_yahoo_com #@UnusedImport

'''

examples['tests/tests/test_example.py'] = '''##########################################################################
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


from tests.flows.search_flows import perform_search
from tests.pages.search_page import ISearchPage
from tests.pages.www_google_com import GoogleSearchPage
from tests.pages.www_yahoo_com import YahooSearchPage
from wtframework.wtf.config import WTF_TIMEOUT_MANAGER
from wtframework.wtf.testobjects.basetests import WTFBaseTest
from wtframework.wtf.web.page import PageFactory
from wtframework.wtf.web.webdriver import WTF_WEBDRIVER_MANAGER
import unittest

# Extend the WTFBaseTest to get access to WTF added features like 
# taking screenshot on test failure.
class Test(WTFBaseTest):


    def tearDown(self):
        "This tear down will close the current allocated webdriver"
        WTF_WEBDRIVER_MANAGER.close_driver()


    def test_basic_example(self):
        "Displays a simple PageObject instantiation example."
        
        # WTF_WEBDRIVER_MANAGER provides a easy to access to 
        # the webdriver.  A web browser will be instantiated 
        # according to your config settings. 
        # - see 'selenium' settings in 'configs/default.yaml'
        webdriver = WTF_WEBDRIVER_MANAGER.new_driver()

        # Simple navigation
        webdriver.get("http://www.google.com")
        
        # Use the PageFactory class to instantiate your page.
        google_page = PageFactory.create_page(GoogleSearchPage, webdriver)
        
        # With your PageObject instantiated, you can call it's methods.
        google_page.search("hello world")
        
        # The WTF_TIMEOUT_MANAGER is handy for inserting configurable waits.
        # In this case we're doing a brief pause to allow the type-ahead search to complete.
        WTF_TIMEOUT_MANAGER.brief_pause() 
        
        self.assertTrue(google_page.result_contains("hello world"))



    def test_example_using_abstract_interfaces(self):
        "Demonstrates creating PageObjects using Abstract Factory pattern."
        webdriver = WTF_WEBDRIVER_MANAGER.new_driver()
        webdriver.get("http://www.google.com")

        
        # Notice I don't need specify GoogleSearchPage specifically, and
        # able to construct a ISearchPage of the correct type.
        search_page = PageFactory.create_page(ISearchPage, webdriver)
        self.assertEqual(GoogleSearchPage, type(search_page))
        
        webdriver.get("http://www.yahoo.com")
        search_page = PageFactory.create_page(ISearchPage, webdriver)
        self.assertEqual(YahooSearchPage, type(search_page))


    def test_using_flows(self):
        "Demonstrate abstracting out several steps into 1 call into a flow"
        webdriver = WTF_WEBDRIVER_MANAGER.new_driver()
        search_page = perform_search("hello world", webdriver)
        self.assertTrue(search_page.result_contains("hello world"))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
'''

examples['tests/tests/test_screen_capture_on_fail.py'] = '''##########################################################################
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

import unittest
from wtframework.wtf.testobjects.basetests import WTFBaseTest
from wtframework.wtf.web.webdriver import WTF_WEBDRIVER_MANAGER


class TestScreenCaptureOnFail(WTFBaseTest):
    """"
    These test cases are expected to fail.  They are here to test 
    the screen capture on failure.
    """

    # Comment out decorator to manually test the screen capture.
    @unittest.expectedFailure
    def test_fail(self):
        driver = WTF_WEBDRIVER_MANAGER.new_driver()
        driver.get('http://www.google.com')
        self.fail()
        #Check your /screenshots folder for a screenshot.

    # Comment out decorator to manually test the screen capture.
    @unittest.expectedFailure
    def test_assert(self):
        driver = WTF_WEBDRIVER_MANAGER.new_driver()
        driver.get('http://www.google.com')
        self.assertEqual(1, 2)
        #Check your /screenshots folder for a screenshot.

    # Comment out decorator to manually test the screen capture.
    @unittest.expectedFailure
    def test_error(self):
        driver = WTF_WEBDRIVER_MANAGER.new_driver()
        driver.get('http://www.google.com')
        raise RuntimeError()
        #Check your /screenshots folder for a screenshot.

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
'''

