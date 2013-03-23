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

from wtframework.wtf.utils.data_utils import generate_timestamped_string, \
    generate_timestamp, generate_random_string
import re
import unittest


class TestDataUtils(unittest.TestCase):


    def test_generateTimeStampedString(self):
        ts_string = generate_timestamped_string("TEST", 5)
        self.assertTrue(len(re.findall(r'^\d{4}-\d{2}-\d{2}_\d{2}\.\d{2}\.\d{2}_TEST_.{5}$', ts_string)) == 1)

    def test_generate_timestamp(self):
        ts_string = generate_timestamp()
        self.assertTrue(len(re.findall(r'^\d{4}-\d{2}-\d{2}_\d{2}\.\d{2}\.\d{2}$', ts_string)) == 1)

    def test_generate_randome_string(self):
        random = generate_random_string(16);
        self.assertEqual(16, len(random))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()