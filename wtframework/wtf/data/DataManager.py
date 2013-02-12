'''
Created on Feb 5, 2013

@author: davidlai
'''
from wtframework.wtf.utils.ProjectUtils import ProjectUtils
import os


class DataManager(object):
    '''
    dataManager
    This class is responsible for providing utilities for accessing 
    test datas, the ones stored in the /datas folder.
    '''
    
    _data_path = None
    
    _DATA_FOLDER_ = "data"

    def __init__(self):
        '''
        Constructor
        '''
        root = ProjectUtils.get_project_root()
        if root[-1] == '/' or root[-1] == '\\':
            self._data_path = ProjectUtils.get_project_root() + DataManager._DATA_FOLDER_
        else:
            self._data_path = ProjectUtils.get_project_root() + "/" + DataManager._DATA_FOLDER_
            
        if not os.path.exists(self._data_path):
            raise RuntimeError("Missing data folder.  Please check to make sure you have a /data directory.")

    
    def get_data_path(self, filename, env_prefix=None):
        "Get data path."
        if env_prefix == None:
            target_file = filename
        else:
            target_file = os.path.join(env_prefix, filename)

        if os.path.exists(os.path.join(self._data_path , target_file) ):
            return os.path.join(self._data_path , target_file)
        else:
            raise dataNotFoundError("Cannot find data: {0}".format(target_file))


class dataNotFoundError(RuntimeError):
    "raised when data cannot be located."
    pass


WTF_DATA_MANAGER = DataManager()