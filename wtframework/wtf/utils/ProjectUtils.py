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
'''
Created on Dec 13, 2012

@author: "David Lai"
'''
#from com import WDProjectRoot
import os
import re


class ProjectUtils:
    '''
    Utility function for gathering information on this project.
    '''

    __root_folder = None

    @staticmethod
    def get_project_root():
        '''
        Return path of the project directory.
        '''
        if(ProjectUtils.__root_folder != None):
            return ProjectUtils.__root_folder

        path = os.getcwd()
        seperator_matches = re.finditer("/|\\\\", path)
        
        paths_to_search = [path]
        for match in seperator_matches:
            p = path[:match.start()]
            paths_to_search.insert(0, p)
        
        for path in paths_to_search:
            if os.path.isfile("{0}/.wtf_root_folder".format(path)):
                ProjectUtils.__root_folder = path + "/"
                return ProjectUtils.__root_folder

        raise RuntimeError("Missing root project folder locator file '.wtf_root_folder'." \
                           + "Check to make sure this file is located in your project directory.")
