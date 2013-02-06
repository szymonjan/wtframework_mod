'''
Created on Feb 6, 2013

@author: davidlai
'''
import unittest
from wtframework.wtf._devtools_.filetemplates import _page_object_template_
from datetime import datetime

class Test(unittest.TestCase):


    def testName(self):
        
        objectmap = "    "+ \
        "objectname = lambda self:self.webdriver.find_element_by_css('.hello')"+\
        "\n"
        
        
        
        print _page_object_template_.content.format(date=datetime.now(),
                                                    url="http://www.google.com",
                                                    pagename="GoogleSearchPage",
                                                    partialurl="/search/",
                                                    objectmap=objectmap)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()