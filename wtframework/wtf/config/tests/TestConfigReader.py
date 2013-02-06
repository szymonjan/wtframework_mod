'''
Created on Dec 13, 2012

@author: David Lai
'''
from wtframework.wtf.config.ConfigReader import ConfigReader
import unittest


class TestConfigReader(unittest.TestCase):


    def test_getValue_ReturnsStringConfigValue(self):
        '''
        Test config value returned is expected value
        '''
        config = ConfigReader("tests/TestConfigReaderData")
        value = config.get_value("string_test")
        self.assertEqual(value, "some value", "Value did not match expected.")

    def test_getValueOrDefault(self):
        "Test the get_value_or_default method returns value if available or the the default."
        config = ConfigReader("tests/TestConfigReaderData")
        self.assertEqual("some value", config.get_value_or_default("string_test", "default value"))
        self.assertEqual("default value", config.get_value_or_default("i_dont_exist", "default value"))

    def test_getValue_ReturnsHandlesMultiLevelKeys(self):
        '''
        Test ConfigReader works with namespaced keys like, path.to.element
        '''
        config = ConfigReader("tests/TestConfigReaderData")
        value = config.get_value("bill-to.given")
        self.assertEqual(value, "Chris", "Value did not match expected.")

    def test_getValue_ReturnsHandlesArrays(self):
        '''
        Test ConfigReader works with YAML arrays.
        '''
        config = ConfigReader("tests/TestConfigReaderData")
        self.assertEqual("dogs", config.get_value("list_test")[0])
        self.assertEqual("cats", config.get_value("list_test")[1])
        self.assertEqual("badgers", config.get_value("list_test")[2])

    def test_getValue_WithMultipleConfigs(self):
        '''
        Test Config reader loaded up with multiple configs loads 
        the config preferences in order.
        '''

        config = ConfigReader("tests/TestConfig2;tests/TestConfig1")
        # should take config from config1
        self.assertEqual("hello", config.get_value("setting_from_config1"))
        # this will take the config from config2, which has precedence.
        self.assertEqual("beautiful", config.get_value("overwrite_setting"))
        # this will take the setting form config2.
        self.assertEqual("hi", config.get_value("setting_from_config2"))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()