#!/usr/bin/env python
"""
Created on Feb 5, 2013

@author: "David Lai"
"""

import os
from optparse import OptionParser
from wtframework.wtf.utils.ProjectUtils import ProjectUtils
from wtframework.wtf.config.ConfigReader import ConfigReader

if __name__ == '__main__':

    usage = "usage: %prog [-options args]"
    parser = OptionParser(usage=usage)
    parser.add_option("-c", "--config", dest="config",
                  help="Config to use (without the .yaml suffix)", metavar="FILE")
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
    if ProjectUtils.get_project_root() not in os.environ["PYTHONPATH"]:
        os.putenv("PYTHONPATH", os.environ["PYTHONPATH"] + os.pathsep + ProjectUtils.get_project_root())

    os.system("nosetests tests/tests/ --with-nosexunit --core-target=reports")
