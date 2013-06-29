'''
Created on Jun 27, 2013

@author: "David Lai"
'''
import unittest
from wtframework.wtf.web.web_utils import BrowserStandBy
import time


class TestWebUtils(unittest.TestCase):


    def test_browserstandby(self):
        fakedriver = WebdriverCallCounterTestStub()
        standby = BrowserStandBy(fakedriver, max_time=10, sleep=1)
        standby.start()
        
        time.sleep(12)
        self.assertGreater(fakedriver.counter, 9)
        self.assertLess(fakedriver.counter, 13)
    
    
    def test_browserstandby_stop(self):
        fakedriver = WebdriverCallCounterTestStub()
        standby = BrowserStandBy(fakedriver, max_time=10, sleep=1)
        standby.start()
        time.sleep(5)
        standby.stop()
        time.sleep(5)
        self.assertGreater(fakedriver.counter, 4)
        self.assertLess(fakedriver.counter, 8)


class WebdriverCallCounterTestStub(object):
    "Lazy Stub for testing"
    def __init__(self):
        self.counter = 0
    
    @property
    def current_url(self):
        self.counter += 1
        return ""

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()