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
Created on Dec 13, 2012

@author: David Lai
'''
from wtframework.wtf.config import ConfigReader
import unittest


class TestConfigReader(unittest.TestCase):


    def test_get_returns_string_config_value(self):
        '''
        Test config value returned is expected value
        '''
        config = ConfigReader("tests/TestConfigReaderData")
        value = config.get("string_test")
        self.assertEqual(value, "some value", "Value did not match expected.")

    def test_get_with_default_value(self):
        "Test the get method returns value if available or the the default."
        config = ConfigReader("tests/TestConfigReaderData")
        self.assertEqual("some value", config.get("string_test", "default value"))
        self.assertEqual("default value", config.get("i_dont_exist", "default value"))

    def test_get_handles_namespaced_keys(self):
        '''
        Test ConfigReader works with namespaced keys like, path.to.element
        '''
        config = ConfigReader("tests/TestConfigReaderData")
        value = config.get("bill-to.given")
        self.assertEqual(value, "Chris", "Value did not match expected.")


    def test_get_handles_yaml_arrays(self):
        '''
        Test ConfigReader works with YAML arrays.
        '''
        config = ConfigReader("tests/TestConfigReaderData")
        self.assertEqual("dogs", config.get("list_test")[0])
        self.assertEqual("cats", config.get("list_test")[1])
        self.assertEqual("badgers", config.get("list_test")[2])

    def test_get_with_cascaded_config_files(self):
        '''
        Test Config reader loaded up with multiple configs loads 
        the config preferences in order.
        '''

        config = ConfigReader("tests/TestConfig2;tests/TestConfig1")
        # should take config from config1
        self.assertEqual("hello", config.get("setting_from_config1"))
        # this will take the config from config2, which has precedence.
        self.assertEqual("beautiful", config.get("overwrite_setting"))
        # this will take the setting form config2.
        self.assertEqual("hi", config.get("setting_from_config2"))
        

    def test_get_with_missing_key_and_no_default(self):
        "An error should be thrown if the key is missing and no default provided."
        config = ConfigReader("tests/TestConfig2;tests/TestConfig1")
        # should take config from config1
        self.assertRaises(KeyError, config.get, "setting_that_doesnt_exist")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()