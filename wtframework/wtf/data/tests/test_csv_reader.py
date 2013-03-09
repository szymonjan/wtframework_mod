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

from wtframework.wtf.data.data_management import CsvReader, WTF_DATA_MANAGER
import unittest


class TestCsvReader(unittest.TestCase):


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