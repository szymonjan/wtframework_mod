content = \
'''
"""

Created on {date}

@author: Your Name Here
"""
import unittest
from wtframework.wtf.wdtestobjects.WTFBaseTest import WTFBaseTest
from wtframework.wtf.web.WebDriverManager import WTF_WEBDRIVER_MANAGER

class {testname}(WTFBaseTest):
    """
    This tests this and that.
    """

    def test_something_does_something(self):
        "Tests something does something"
        webdriver = WTF_WEBDRIVER_MANAGER.get_driver()
        
        # do some test stuff here.
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
'''