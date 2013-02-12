'''
Created on Feb 8, 2013

@author: davidlai
'''
import unittest
from wtframework.wtf.testobjects.TestCase import TestCase
from wtframework.wtf.testobjects.WTFDataDriven import csvdata
from ddt import ddt

@ddt
class TestCsvDataDrivenTest(TestCase):

    expected_animals = ['Dog', 'Cat', 'Lizzard']
    
    @csvdata("testdata.csv", "testenv")
    def test_csv_datadriven(self, entry):
        print "Saw entry:", entry
        TestCsvDataDrivenTest.expected_animals.remove(entry['Animal'])

    def test_zzz_check_if_datadriven_test_all_ran(self):
        self.assertEqual(0, len(TestCsvDataDrivenTest.expected_animals))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()