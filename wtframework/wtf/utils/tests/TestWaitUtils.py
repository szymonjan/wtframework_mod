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
'''
Created on Dec 28, 2012

@author: "David Lai"
'''
from datetime import datetime, timedelta
from wtframework.wtf.utils.WaitUtils import WaitUtils, OperationTimeoutError
import unittest


class TestWaitUtils(unittest.TestCase):


    def test_waitUntil_returnsAfterConditionsMet(self):
        "Test wait until condition=true works."
        # create a condition that returns true after 2 seconds.
        end_time = datetime.now() + timedelta(seconds = 2)
        too_long = end_time + timedelta(seconds = 2)
        condition = lambda: datetime.now() > end_time
        
        WaitUtils.wait_until(condition, 4, 0.5)
        self.assertLess(datetime.now(), too_long)

    def test_waitUntil_raisesErrorIfTimedOut(self):
        "Test that wait timeout throws error after timeout period."
        # create a condition that returns true after 2 seconds.
        not_long_enough = datetime.now() + timedelta(seconds = .2)
        too_long = not_long_enough + timedelta(seconds = 2)
        condition = lambda: False
        try:
            WaitUtils.wait_until(condition, 1, 0.5)
        except OperationTimeoutError:
            now = datetime.now()
            self.assertGreater(now, not_long_enough)
            self.assertLess(now, too_long)
        except:
            self.fail("OperationTimeoutError expected.")



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()