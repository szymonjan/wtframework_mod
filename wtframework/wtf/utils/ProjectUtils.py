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
