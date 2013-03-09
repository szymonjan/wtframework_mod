'''
Created on Mar 6, 2013

@author: "David Lai"
'''
import unittest
from wtframework.wtf.config import ConfigReader
from wtframework.wtf.config import TimeOutManager


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