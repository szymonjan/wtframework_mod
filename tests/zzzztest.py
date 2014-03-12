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
from wtframework.wtf.web.webdriver import WTF_WEBDRIVER_MANAGER
class Test(unittest.TestCase):


    def testName(self):
        driver = WTF_WEBDRIVER_MANAGER.new_driver()
        print("hello")


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