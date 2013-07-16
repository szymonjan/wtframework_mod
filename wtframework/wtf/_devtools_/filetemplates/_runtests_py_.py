content = \
'''#!/usr/bin/env python
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
from wtframework.wtf.config import ConfigReader
from wtframework.wtf.utils.project_utils import ProjectUtils
import os


if __name__ == '__main__':

    usage = "usage: %prog [-options args]"
    parser = OptionParser(usage=usage)
    parser.add_option("-c", "--config", dest="config",
                  help="Config to use (without the .yaml suffix)", metavar="FILE")
    parser.add_option("-r", "--results", dest="result_file",
                  help="path to create result file.", metavar="FILE")
    (options, args) = parser.parse_args()


    if options.config:
        # check if config exists.
        if os.path.exists(ProjectUtils.get_project_root() + \
                          ConfigReader.CONFIG_LOCATION + options.config +\
                          ConfigReader.CONFIG_EXT):
            print "Setting config WTF_ENV to:", options.config
            os.putenv(ConfigReader.ENV_VARS, options.config)
        else:
            print "Cannot find config: ", ProjectUtils.get_project_root() + \
                          ConfigReader.CONFIG_LOCATION + options.config +\
                          ConfigReader.CONFIG_EXT

    # Set PYTHONPATH if not set.
    try:
        if ProjectUtils.get_project_root() not in os.environ["PYTHONPATH"]:
            os.putenv("PYTHONPATH", os.environ["PYTHONPATH"] + os.pathsep + ProjectUtils.get_project_root())
    except:
        os.putenv("PYTHONPATH", ProjectUtils.get_project_root())

    if options.result_file:
        result_path = options.result_file
    else:
        result_path = os.path.join("reports", "results.xml")
    os.system("nosetests-2.7 tests/tests/ --with-xunit --xunit-file={0}".format(result_path))




'''