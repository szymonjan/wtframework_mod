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
from wtframework.wtf.config import ConfigReader, TimeOutManager
import unittest


class TestTimeOutManager(unittest.TestCase):


    def setUp(self):
        config_reader = ConfigReader('tests/timeout-manager-testfile')
        self.timeout_manager = TimeOutManager(config_reader=config_reader)
    
    def tearDown(self):
        self.timeout_manager = None
    
    def test_timeout_manager_grabs_value_from_config_file(self):
        "Test timeout manager returns value from our timeout settings."
        self.assertEqual(6, self.timeout_manager.BRIEF)
        self.assertEqual(11, self.timeout_manager.SHORT)
        self.assertEqual(31, self.timeout_manager.NORMAL)
        self.assertEqual(61, self.timeout_manager.LONG)
        self.assertEqual(301, self.timeout_manager.EPIC)
    
    def test_timeout_manager_uses_default_value_when_not_specified_in_config(self):
        "Test timeout manager returns value from our timeout settings."
        config_reader = ConfigReader('tests/TestConfig1')
        timeout_manager = TimeOutManager(config_reader=config_reader)
        
        self.assertEqual(5, timeout_manager.BRIEF)
        self.assertEqual(10, timeout_manager.SHORT)
        self.assertEqual(30, timeout_manager.NORMAL)
        self.assertEqual(60, timeout_manager.LONG)
        self.assertEqual(300, timeout_manager.EPIC)



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()