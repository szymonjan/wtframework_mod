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
from wtframework.wtf.utils.wait_utils import wait_until, OperationTimeoutError,\
    do_until
import unittest




class TestWaitUtils(unittest.TestCase):


    def test_wait_until_returnsAfterConditionsMet(self):
        "Test wait until condition=true works."
        # create a condition that returns true after 2 seconds.
        end_time = datetime.now() + timedelta(seconds = 2)
        too_long = end_time + timedelta(seconds = 2)
        condition = lambda: datetime.now() > end_time
        
        wait_until(condition, 4, 0.5)
        self.assertLess(datetime.now(), too_long)

    def test_wait_until_raisesErrorIfTimedOut(self):
        "Test that wait timeout throws error after timeout period."
        # create a condition that returns true after 2 seconds.
        not_long_enough = datetime.now() + timedelta(seconds = .2)
        too_long = not_long_enough + timedelta(seconds = 2)
        condition = lambda: False
        try:
            wait_until(condition, 1, 0.5)
        except OperationTimeoutError:
            now = datetime.now()
            self.assertGreater(now, not_long_enough)
            self.assertLess(now, too_long)
        except:
            self.fail("OperationTimeoutError expected.")
        

    def test_wait_until_with_pass_exception_option(self):
        condition = lambda: 1/0
        try :
            wait_until(condition, pass_exceptions=True)
            raise Exception("Test Failed, exception should be thrown.")
        except ZeroDivisionError:
            #Means the error was passed through as expected.
            pass
        except Exception as e:
            #Means we got the wrong error.
            raise e


    def test_do_until_retries_until_action_successful(self):
        self.__x = 0
        do_until(lambda: self.__wait_condition())
        self.assertEqual(2, self.__x)

    def __wait_condition(self):
        self.__x += 1
        if self.__x < 2:
            raise RuntimeError("error")

    def test_do_until_raises_exeption_when_timeout(self):
        self.assertRaises(OperationTimeoutError, do_until, lambda: 1/0, 1 )





if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()