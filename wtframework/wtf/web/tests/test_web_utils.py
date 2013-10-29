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
from wtframework.wtf.web.web_utils import BrowserStandBy
import time
import unittest2


class TestWebUtils(unittest2.TestCase):


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


    def test_browserstandby_withstmt(self):
        fakedriver = WebdriverCallCounterTestStub()

        with BrowserStandBy.start_standby(fakedriver, max_time=10, sleep=1):
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
    unittest2.main()