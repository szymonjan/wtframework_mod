#!/usr/bin/env python
'''
Created on Feb 4, 2013

@author: "David Lai"
'''
from optparse import OptionParser





################# MAIN SCRIPT ######################
if __name__ == '__main__':
        
    usage = "usage: %prog command argument1"
    parser = OptionParser(usage=usage)

    (options, args) = parser.parse_args()
    print options
    print args

    if len(args) < 2:
        print "Invalid command.", usage
        exit(1)
        
    if args[0] == "generate-page":
        url = args[1]
        print "Generating page object for url:", url
    else:
        print "Invalid command.", usage, "\nFor help:\nwtf_tools.py --help\n"

