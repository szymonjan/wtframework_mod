from six import u


contents = u(\
'''#!/usr/bin/env python
##########################################################################
# This file is part of WTFramework. 
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

from __future__ import print_function
from optparse import OptionParser
from wtframework.wtf.constants import WTF_CONFIG_LOCATION, WTF_CONFIG_EXT, \\
    WTF_ENV_VARS
from wtframework.wtf.utils.project_utils import ProjectUtils
import os
import re


if __name__ == '__main__':

    usage = "usage: %prog [-options args]"
    parser = OptionParser(usage=usage)
    parser.add_option("-c", "--config", dest="config",
                  help="Config to use (without the .yaml suffix)", metavar="FILE")
    parser.add_option("-r", "--results", dest="result_file",
                  help="path to create result file.", metavar="FILE")
    (options, args) = parser.parse_args()


    if options.config:
        configs = re.split(",|;", options.config)
        configs_valid = True
        for config in configs:
            # check if config exists.
            expected_path = os.path.join(ProjectUtils.get_project_root(),
                                         WTF_CONFIG_LOCATION,
                                         config + WTF_CONFIG_EXT)
            if os.path.exists(expected_path):
                pass  # config exists.
            else:
                configs_valid = False
                print("Cannot find config: ", expected_path)
        
        if configs_valid:
            os.putenv(WTF_ENV_VARS, options.config)
            print("Setting config WTF_ENV to:", options.config)
        else:
            exit(1)  # one or more errors was found in the configs.
        

    # Set PYTHONPATH if not set.
    try:
        if ProjectUtils.get_project_root() not in os.environ["PYTHONPATH"]:
            os.putenv("PYTHONPATH", os.path.join(os.environ["PYTHONPATH"], ProjectUtils.get_project_root()))
    except:
        os.putenv("PYTHONPATH", ProjectUtils.get_project_root())

    if options.result_file:
        result_path = options.result_file
    else:
        result_path = os.path.join("reports", "results.xml")
    test_path = os.path.join("tests", "tests") + os.pathsep
    os.system("nosetests-2.7 {test_path} --with-xunit --xunit-file={result_path}"\\
              .format(result_path=result_path, test_path=test_path))



''')