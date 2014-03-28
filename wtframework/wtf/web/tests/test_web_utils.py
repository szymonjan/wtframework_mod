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
from datetime import datetime, timedelta
import time

import unittest2
from wtframework.wtf.utils.test_utils import do_and_ignore
from wtframework.wtf.web.web_utils import BrowserStandBy, WebUtils
from wtframework.wtf.web.webdriver import WTF_WEBDRIVER_MANAGER


class TestWebUtils(unittest2.TestCase):

    def setUp(self):
        self.webdriver = WTF_WEBDRIVER_MANAGER.new_driver("TestWebUtils")

    def tearDown(self):
        do_and_ignore(lambda: WTF_WEBDRIVER_MANAGER.close_driver())

    def test_check_url(self):
        result, resp = WebUtils.check_url("http://the-internet.herokuapp.com/status_codes/200")
        self.assertTrue(result)
        self.assertEqual(200, resp)

    def test_check_url_bad_url_case(self):
        result, resp = WebUtils.check_url("http://the-internet.herokuapp.com/status_codes/404")
        self.assertFalse(result)
        self.assertEqual(404, resp)

    def test_get_base_url(self):
        self.webdriver.get("http://the-internet.herokuapp.com/status_codes/200")
        base_url = WebUtils.get_base_url(self.webdriver)
        self.assertEqual("http://the-internet.herokuapp.com", base_url)


    def test_get_browser_datetime(self):
        browser_time = WebUtils.get_browser_datetime(self.webdriver)
        local_time = datetime.now()
        time_difference = abs(local_time - browser_time)
        self.assertLess(time_difference, timedelta(days=1))


    def test_row_to_dictionary(self):
        self.webdriver.get("http://the-internet.herokuapp.com/tables")

        header = self.webdriver.find_element_by_css_selector("#table1 thead tr")
        target_row = self.webdriver.find_element_by_css_selector("#table1 tbody tr")

        row_values = WebUtils.row_to_dictionary(header, target_row)
        self.assertEqual("Smith", row_values['Last Name'])
        self.assertEqual("jsmith@gmail.com", row_values['Email'])
        self.assertEqual("http://www.jsmith.com", row_values['Web Site'])


class TestWebBrowserStandBy(unittest2.TestCase):

    def test_browserstandby(self):
        fakedriver = WebdriverCallCounterTestStub()
        standby = BrowserStandBy(fakedriver, max_time=10, sleep=1)
        standby.start()

        time.sleep(12)
        self.assertGreater(fakedriver.counter, 9)
        self.assertLess(fakedriver.counter, 13)

    def test_browserstandby_stop(self):
        fakedriver = WebdriverCallCounterTestStub()
        standby = BrowserStandBy(fakedriver, max_time=10, sleep=1)
        standby.start()
        time.sleep(5)
        standby.stop()
        time.sleep(5)
        self.assertGreater(fakedriver.counter, 4)
        self.assertLess(fakedriver.counter, 8)

    def test_browserstandby_withstmt(self):
        fakedriver = WebdriverCallCounterTestStub()

        with BrowserStandBy.start_standby(fakedriver, max_time=10, sleep=1):
            time.sleep(5)

        self.assertGreater(fakedriver.counter, 4)
        self.assertLess(fakedriver.counter, 8)


class WebdriverCallCounterTestStub(object):

    "Lazy Stub for testing"

    def __init__(self):
        self.counter = 0

    # Note: This bit of code is tied to the implementation details, since we 
    # we're using the current_url as the keep alive mechanism.
    @property
    def current_url(self):
        self.counter += 1
        return ""

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest2.main()
