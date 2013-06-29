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
from wtframework.wtf.utils.test_utils import do_and_ignore
from wtframework.wtf.web import page
from wtframework.wtf.web.page import PageObject, InvalidPageError, \
    PageLoadTimeoutError
from wtframework.wtf.web.webdriver import WTF_WEBDRIVER_MANAGER
import threading
import time
import unittest

class GoogleSearch(PageObject):
    
    def _validate_page(self, webdriver):
        if not "google.com" in webdriver.current_url:
            raise InvalidPageError("Not google.")



class TestPageUtils(unittest.TestCase):

    def tearDown(self):
        self._mocker = None

        #tear down any webdrivers we create.
        do_and_ignore(lambda: WTF_WEBDRIVER_MANAGER.close_driver())


    def __load_google_later(self):
        print "load google later thread started."
        time.sleep(10)
        self.driver.get("http://www.google.com")
        print "load google later thread now loading google."

    def test_wait_for_page_to_load(self):
        self.driver = WTF_WEBDRIVER_MANAGER.new_driver("TestPageUtils.test_wait_for_page_to_load")
        start_time = datetime.now()
        self.driver.get("http://www.yahoo.com")
        
        # create a separate thread to load yahoo 10 seconds later.
        t = threading.Thread(target=self.__load_google_later())
        t.start()

        self.page_obj = page.PageUtils.wait_until_page_loaded(GoogleSearch, self.driver, 60)
        
        end_time = datetime.now()
        
        # check we get a page object pack.
        self.assertTrue(isinstance(self.page_obj, GoogleSearch))
        # check that the instantiation happened later when the page was loaded.
        self.assertGreater(end_time - start_time, timedelta(seconds=10))

   
    def test_wait_for_page_loads_times_out_on_bad_page(self):
        self.driver = WTF_WEBDRIVER_MANAGER.new_driver("TestPageUtils.test_wait_for_page_loads_times_out_on_bad_page")
        self.driver.get("http://www.yahoo.com")
        self.assertRaises(PageLoadTimeoutError, page.PageUtils.wait_until_page_loaded, GoogleSearch, self.driver, 1)


    def test_wait_for_page_loads_times_out_on_bad_page_list(self):
        self.driver = WTF_WEBDRIVER_MANAGER.new_driver("TestPageUtils.test_wait_for_page_loads_times_out_on_bad_page_list")
        self.driver.get("http://www.yahoo.com")
        self.assertRaises(PageLoadTimeoutError, page.PageUtils.wait_until_page_loaded, 
                          [GoogleSearch], self.driver, 1)



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()