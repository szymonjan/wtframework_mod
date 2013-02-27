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
Created on Feb 5, 2013

@author: davidlai
'''
import unittest
from wtframework.wtf.assettools.AssetManager import AssetManager
import os


class TestAssetManager(unittest.TestCase):


    def test_asset_manager_returns_filepath(self):
        file_path = AssetManager().get_asset_path("a_test_file.txt")
        self.assertTrue(os.path.exists(file_path), \
                        "Expecting 'a_test_file.txt to be under /assets folder.")

    def test_get_asset_path_throws_error_if_file_not_exist(self):
        self.assertRaises(Exception, AssetManager().get_asset_path, "i_do_not_exist_.text")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()