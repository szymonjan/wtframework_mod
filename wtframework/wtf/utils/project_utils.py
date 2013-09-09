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

import os
import re


class ProjectUtils(object):
    """
    Utility methods for working with the project.
    
    """


    __root_folder__ = None

    @classmethod
    def get_project_root(cls):
        '''
        Return path of the project directory.  Use this method for getting paths relative to the project.
        However, for data, it's recommended you use WTF_DATA_MANAGER and for assets it's recommended 
        to use WTF_ASSET_MANAGER, which are already singleton instances that manger the /data, and /assets 
        folder for you.
        
        Returns:
            str - path of project root directory.
        '''
        if(cls.__root_folder__ != None):
            return cls.__root_folder__

        path = os.getcwd()
        seperator_matches = re.finditer("/|\\\\", path)

        paths_to_search = [path]
        for match in seperator_matches:
            p = path[:match.start()]
            paths_to_search.insert(0, p)

        for path in paths_to_search:
            if os.path.isfile("{0}/.wtf_root_folder".format(path)):
                cls.__root_folder__ = path + "/"
                return cls.__root_folder__

        raise RuntimeError("Missing root project folder locator file '.wtf_root_folder'." \
                           + "Check to make sure this file is located in your project directory.")

