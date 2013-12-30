'''
Created on Jun 27, 2013

@author: davidlai
'''
from selenium import webdriver
import time
import unittest
#from selenium.common.exceptions import WebDriverException
#from selenium.webdriver.common import utils
#import os
#import selenium
#import subprocess


import wtframework.wtf.web.page
class Test(unittest.TestCase):


    def testName(self):
#        #self.process = subprocess.Popen(['/usr/bin/env', 'phantomjs', '--webdriver=59202'])
#        selenium.webdriver.phantomjs.service.Service.start = self._start
#        driver = webdriver.PhantomJS()
        driver = webdriver.Firefox()
        driver.get("http://www.github.com")
        search_input = lambda: driver.find_element_by_name('q')
        search_input().send_keys('hello world\n') 
        time.sleep(5)
        search_input().send_keys('hello frank\n') # no stale element exception


#    def _start(self):
#        """
#        Starts PhantomJS with GhostDriver.
#
#        :Exceptions:
#         - WebDriverException : Raised either when it can't start the service
#           or when it can't connect to the service
#        """
#        try:
#            self.process = subprocess.Popen(['/usr/bin/env'] + self.service_args,
#                                            stdout=self._log, stderr=self._log)
#        except Exception as e:
#            raise WebDriverException("Unable to start phantomjs with ghostdriver.", e)
#        count = 0
#        while not utils.is_connectable(self.port):
#            count += 1
#            time.sleep(1)
#            if count == 30:
#                raise WebDriverException("Can not connect to GhostDriver")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()