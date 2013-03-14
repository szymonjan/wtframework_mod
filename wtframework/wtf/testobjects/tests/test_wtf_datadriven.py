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
Created on Feb 8, 2013

@author: davidlai
'''
import unittest
from wtframework.wtf.testobjects.test_decorators import csvdata
from ddt import ddt
from wtframework.wtf.testobjects.testcase import WatchedTestCase


@ddt
class TestCsvDataDrivenTest(WatchedTestCase):

    expected_animals = ['Dog', 'Cat', 'Lizzard']
    
    
    @csvdata("testdata.csv", "testenv")
    def test_csv_datadriven(self, entry):
        "Test a CSV data driven test runs tests for each data entry."
        print "Saw entry:", entry
        self.expected_animals.remove(entry['Animal'])

    def test_zzz_check_if_datadriven_test_all_ran(self):
        self.assertEqual(0, len(self.expected_animals))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()