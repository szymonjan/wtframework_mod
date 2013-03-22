'''
Created on Mar 8, 2013

@author: "David Lai"
'''
import unittest
from wtframework.wtf.web import page
from selenium import webdriver
from wtframework.wtf.web.page import PageObject, InvalidPageError,\
    PageLoadTimeoutError
from datetime import datetime, timedelta
import threading
import time

class GoogleSearch(PageObject):
    
    def _validate_page(self, webdriver):
        if not "google.com" in webdriver.current_url:
            raise InvalidPageError("Not google.")



class TestPageUtils(unittest.TestCase):

    def tearDown(self):
        self._mocker = None

        #tear down any webdrivers we create.
        try:
            self.driver.close()
        except:
            pass

    def __load_google_later(self):
        print "load google later thread started."
        time.sleep(10)
        self.driver.get("http://www.google.com")
        print "load google later thread now loading google."

    def test_wait_for_page_to_load(self):
        self.driver = webdriver.Firefox()
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
        self.driver = webdriver.Firefox()
        self.driver.get("http://www.yahoo.com")
        self.assertRaises(PageLoadTimeoutError, page.PageUtils.wait_until_page_loaded, GoogleSearch, self.driver, 1)


    def test_wait_for_page_loads_times_out_on_bad_page_list(self):
        self.driver = webdriver.Firefox()
        self.driver.get("http://www.yahoo.com")
        self.assertRaises(PageLoadTimeoutError, page.PageUtils.wait_until_page_loaded, 
                          [GoogleSearch], self.driver, 1)



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()