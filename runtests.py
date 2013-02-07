#!/usr/bin/env python
"""
Created on Feb 5, 2013

@author: "David Lai"
"""

import os
from optparse import OptionParser

if __name__ == '__main__':

    usage = "usage: %prog "
    parser = OptionParser(usage=usage)
    #TODO option for rerunning failed tests.
    
    os.system("nosetests tests/ --with-nosexunit --core-target=reports")
