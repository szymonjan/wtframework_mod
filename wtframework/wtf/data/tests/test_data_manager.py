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

from wtframework.wtf.data.data_management import DataManager
import os
import unittest


class TestDataManager(unittest.TestCase):


    def test_data_manager_returns_filepath(self):
        file_path = DataManager().get_data_path("testdata.csv", "testenv")
        self.assertTrue(os.path.exists(file_path), \
                        "Expecting 'testdata.csv' to be under /data/testenv folder.")

    def test_data_manager_returns_filepath_without_env(self):
        file_path = DataManager().get_data_path("testdata1.csv")
        self.assertTrue(os.path.exists(file_path), \
                        "Expecting 'testdata1.csv' to be under /data/ folder.")


    def test_data_manager_throws_error_when_data_not_found(self):
        self.assertRaises(RuntimeError, DataManager().get_data_path, "testnodata.csv", "testenv")
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()