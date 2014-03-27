##########################################################################
# This file is part of WTFramework.
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
import unittest2
from wtframework.wtf.utils.test_utils import do_and_ignore, do_if_match

class TestTestUtils(unittest2.TestCase):


    def test_do_and_ignore(self):
        self.__did_call_function = False
        def erroneous_func():
            self.__did_call_function = True
            raise RuntimeError("IGNORE ME")

        do_and_ignore(lambda: erroneous_func())
        self.assertTrue(self.__did_call_function)


    def test_do_if_match(self):
        self.__magic_number = None
        numbers = [1, 3, 4, 5, 6]
        matcher = lambda num: num % 2 == 0
        
        def target_action(item):
            self.__magic_number = item
        
        do_if_match(numbers, matcher, target_action)
        self.assertEqual(4, self.__magic_number)



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest2.main()