'''
Created on Feb 6, 2013

@author: davidlai
'''
from datetime import datetime
from wtframework.wtf._devtools_.filetemplates import _test_template_

def generate_empty_test(test_name):
    "Generates an empty test extending WTFBaseTest"
    date = datetime.now()
    return _test_template_.content.format(date=date, testname=test_name)