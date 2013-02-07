#!/usr/bin/env python
'''
Created on Feb 4, 2013

@author: "David Lai"
'''
from optparse import OptionParser
from wtframework.wtf._devtools_ import page_object_tools, test_generation_tools
import os
from wtframework.wtf.utils.ProjectUtils import ProjectUtils


def create_file(filepath, contents):
    if not os.path.exists(filepath):
        print "Creating {0}".format(filepath)
        text_file = open(filepath, "w")
        text_file.write(contents)
        text_file.close()
    else:
        print "{0} already exists.".format(filepath)


################# MAIN SCRIPT ######################
if __name__ == '__main__':
        
    usage = "usage: %prog command arg1 arg2 ..."
    parser = OptionParser(usage=usage)

    (options, args) = parser.parse_args()
    print options
    print args

    if len(args) < 2:
        print "Invalid command.", usage
        exit(1)
        
    if args[0] == "generate-page":
        if len(args) < 3:
            raise RuntimeError("usage: wtf_tools.py generate-page PageName http://page.url.com/somepage")

        pagename = args[1]
        url = args[2]
        print "Generating page object for url:", url
        file_content = page_object_tools.generate_page_object(pagename, url)
        create_file(ProjectUtils.get_project_root() \
                    +"tests/pages/{pagename}.py".format(pagename=pagename), file_content)

    elif args[0] == "generate-test":
        test_name = args[1]
        print "Generating generic test."
        file_content = test_generation_tools.generate_empty_test(test_name)
        create_file(ProjectUtils.get_project_root() \
                    +"tests/tests/{test_name}.py".format(test_name=test_name),\
                    file_content)
        
    else:
        print "Invalid command.", usage, "\nFor help:\nwtf_tools.py --help\n"

