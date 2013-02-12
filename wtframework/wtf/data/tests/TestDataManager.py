'''
Created on Feb 5, 2013

@author: davidlai
'''
from wtframework.wtf.data.DataManager import DataManager
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