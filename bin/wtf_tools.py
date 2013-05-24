#!/usr/bin/env python
##########################################################################
#This file is part of WTFramework. 
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


from optparse import OptionParser
from wtframework.wtf._devtools_ import page_object_tools, test_generation_tools
from wtframework.wtf.utils.project_utils import ProjectUtils
import os
import wtframework


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
    parser.add_option("--version", action="store_true",
                      default=False, dest="version_flag",
                      help="Version info.")

    (options, args) = parser.parse_args()

    if(options.version_flag):
        print wtframework.__VERSION__
        exit()

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
                    +"tests/pages/{pagename}.py".format(pagename=pagename.lower()), file_content)

    elif args[0] == "generate-test":
        test_name = args[1]
        print "Generating generic test."
        file_content = test_generation_tools.generate_empty_test(test_name)
        create_file(ProjectUtils.get_project_root() \
                    +"tests/tests/{test_name}.py".format(test_name=test_name),\
                    file_content)
        
    else:
        print "Invalid command.", usage, "\nFor help:\nwtf_tools.py --help\n"

