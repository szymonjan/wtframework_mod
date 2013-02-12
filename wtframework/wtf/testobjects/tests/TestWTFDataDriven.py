'''
Created on Feb 8, 2013

@author: davidlai
'''
import unittest
from wtframework.wtf.testobjects.WTFDataDriven import csvdata
from ddt import ddt
from wtframework.wtf.testobjects.WatchedTestCase import WatchedTestCase


@ddt
class TestCsvDataDrivenTest(WatchedTestCase):

    expected_animals = ['Dog', 'Cat', 'Lizzard']
    
    @csvdata("testdata.csv", "testenv")
    def test_csv_datadriven(self, entry):
        print "Saw entry:", entry
        self.expected_animals.remove(entry['Animal'])

    def test_zzz_check_if_datadriven_test_all_ran(self):
        self.assertEqual(0, len(self.expected_animals))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()