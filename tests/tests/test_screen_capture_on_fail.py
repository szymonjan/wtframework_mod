##########################################################################
# This file is part of WTFramework.
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

from wtframework.wtf.testobjects.basetests import WTFBaseTest
from wtframework.wtf.web.webdriver import WTF_WEBDRIVER_MANAGER
import unittest


class TestScreenCaptureOnFail(WTFBaseTest):

    """"
    These test cases are expected to fail.  They are here to test 
    the screen capture on failure.

    To see these running, comment out the 'expectedFailure' 
    decorators, then run them.  Upon failures, you should see 
    screenshots generated in the /screenshots folder.
    """

    # Comment out decorator to manually test the screen capture.
    @unittest.expectedFailure
    def test_fail(self):
        driver = WTF_WEBDRIVER_MANAGER.new_driver()
        driver.get('http://www.google.com')
        self.fail()
        # Check your /screenshots folder for a screenshot.

    # Comment out decorator to manually test the screen capture.
    @unittest.expectedFailure
    def test_assert(self):
        driver = WTF_WEBDRIVER_MANAGER.new_driver()
        driver.get('http://www.google.com')
        self.assertEqual(1, 2)
        # Check your /screenshots folder for a screenshot.

    # Comment out decorator to manually test the screen capture.
    @unittest.expectedFailure
    def test_error(self):
        driver = WTF_WEBDRIVER_MANAGER.new_driver()
        driver.get('http://www.google.com')
        raise RuntimeError()
        # Check your /screenshots folder for a screenshot.

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
