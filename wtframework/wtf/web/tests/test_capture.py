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
import imghdr
import os
import unittest2
from wtframework.wtf.utils.project_utils import ProjectUtils
from wtframework.wtf.web.capture import WebScreenShotUtil
from wtframework.wtf.web.webdriver import WTF_WEBDRIVER_MANAGER
from wtframework.wtf.utils.test_utils import do_and_ignore


class TestCapture(unittest2.TestCase):

    def tearDown(self):
        # tear down any webdrivers we create.
        do_and_ignore(lambda: WTF_WEBDRIVER_MANAGER.close_driver())

    def test_capture_file_created_and_valid_png(self):
        self.driver = WTF_WEBDRIVER_MANAGER.new_driver(
            "TestPageUtils.test_capture_file_created_and_valid_png")
        self.driver.get("http://www.yahoo.com")
        fname = "test"
        prj_root = ProjectUtils.get_project_root()
        fpath = os.path.join(
            prj_root, WebScreenShotUtil.SCREEN_SHOT_LOCATION, fname + ".png")
        try:
            WebScreenShotUtil.take_screenshot(self.driver, fname)
            self.assertTrue(os.path.isfile(fpath))
            self.assertEquals(imghdr.what(fpath), "png")
        finally:
            try:
                os.remove(fpath)
            except OSError:
                pass
