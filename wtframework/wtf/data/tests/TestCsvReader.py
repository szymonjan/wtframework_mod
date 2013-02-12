'''
Created on Feb 11, 2013

@author: davidlai
'''
import unittest
from wtframework.wtf.data.CsvReader import CsvReader
from wtframework.wtf.data.DataManager import WTF_DATA_MANAGER


class Test(unittest.TestCase):


    def test_csv_reader_reads_csv_file(self):
        csvreader = CsvReader(WTF_DATA_MANAGER.get_data_path("testdata.csv", "testenv"))
        first_row = csvreader.next()
        self.assertEqual("Dog", first_row['Animal'])
        self.assertEqual("3.0", first_row['Size'])

        second_row = csvreader.next()
        self.assertEqual("Cat", second_row['Animal'])
        self.assertEqual("Mammal", second_row['Type'])

        third_row = csvreader.next()
        self.assertEqual("Reptile", third_row['Type'])
        self.assertEqual("2.0", third_row['Size'])

        self.assertRaises(StopIteration, csvreader.next)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()