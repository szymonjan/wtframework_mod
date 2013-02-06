'''
Created on Jan 31, 2013

@author: "David Lai"
'''
from wtframework.wtf.utils.DataUtils import DataUtils
import re
import unittest


class Test(unittest.TestCase):


    def test_generateTimeStampedString(self):
        ts_string = DataUtils.generate_timestamped_string("TEST", 5)
        self.assertTrue(len(re.findall(r'^\d{4}-\d{2}-\d{2}_\d{2}\.\d{2}\.\d{2}_TEST_.{5}$', ts_string)) == 1)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()