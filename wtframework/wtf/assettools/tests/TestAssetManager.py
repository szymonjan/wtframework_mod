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


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()