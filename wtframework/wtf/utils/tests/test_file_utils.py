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

from wtframework.wtf.utils import file_utils
import tempfile
import unittest2


class TestFileUtils(unittest2.TestCase):


    def test_generate_temp_path(self):
        "Tests creating a file in temp directory."
        temp_name = file_utils.temp_path("blah")
        self.assertTrue( tempfile.gettempdir() in temp_name)

    def test_create_temp_file_creates_file_with_desired_content(self):
        "Tests tempfile is created with desired contents."
        temp_file = file_utils.create_temp_file(string_or_another_file="hello world")
        temp_file_contents = open(temp_file).read()
        self.assertEqual("hello world", temp_file_contents)

    def test_download_to_tempfile_downloads_content(self):
        "Test file is downloaded to temp file correctly"
        # This is a data URI that has a URL encoded text "hello world"
        hello_world_data_uri = "data:text/plain;charset=utf-8;base64,aGVsbG8gd29ybGQ="
        
        temp_file = file_utils.download_to_tempfile(hello_world_data_uri)
        temp_file_contents = open(temp_file).read()
        
        self.assertEqual("hello world", temp_file_contents) 




if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest2.main()