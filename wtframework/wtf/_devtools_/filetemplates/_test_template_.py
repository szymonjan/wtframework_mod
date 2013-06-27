content = \
'''
"""

Created on {date}

@author: Your Name Here
"""
from wtframework.wtf.testobjects.basetests import WTFBaseTest
from wtframework.wtf.web.webdriver import WTF_WEBDRIVER_MANAGER
import unittest

class {testname}(WTFBaseTest):
    """
    This tests this and that.
    """

    def setUp(self):

    def test_something_does_something(self):
        "Tests something does something"
        webdriver = WTF_WEBDRIVER_MANAGER.new_driver()
        
        # do some test stuff here.
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
'''