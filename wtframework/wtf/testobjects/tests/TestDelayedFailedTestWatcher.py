'''
Created on Feb 13, 2013

@author: "David Lai"
'''
import unittest
from wtframework.wtf.testobjects.WTFBaseTest import WTFBaseTest

# Using WTFBaseTest since it already consumes this test Watcher.
class Test(WTFBaseTest):

    # Note, this test is expected to fail, we want to check if we get 1 exception
    # that embeds the 3 exceptions from the failed asserts.
    # To test this, uncomment out the unittest.skipTest decorator.
    # Then check the exception thrown to see if it includes the 3 exceptions we 
    # delayed failure on.
    @unittest.SkipTest
    def test_delayed_test_fail(self):
        "Check that delayed test failures are raised at the end of a test."
        # all 3 are expected to fail, but look in the log message to check for the "Test Passed" message
        self.assertWithDelayedFailure(self.assertEqual, 1, 2)
        self.assertWithDelayedFailure(self.assertTrue, False)
        self.assertWithDelayedFailure(self.assertGreater, 1, 2)
        print "Test ran all the way through.  Now check the console log to make sure "

    def test_delayed_test_pass(self):
        "Check that when assertions pass, no error is thrown afterwards."
        # all 3 are expected to fail, but look in the log message to check for the "Test Passed" message
        self.assertWithDelayedFailure(self.assertEqual, 1, 1)
        self.assertWithDelayedFailure(self.assertTrue, True)
        self.assertWithDelayedFailure(self.assertGreater, 2, 1)
        print "Test ran all the way through.  Now check the console log to make sure "


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()