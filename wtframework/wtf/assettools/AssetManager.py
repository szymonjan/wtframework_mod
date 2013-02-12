'''
Created on Feb 5, 2013

@author: davidlai
'''
from wtframework.wtf.utils.ProjectUtils import ProjectUtils
import os


class AssetManager(object):
    '''
    AssetManager
    This class is responsible for providing utilities for accessing 
    test assets, the ones stored in the /assets folder.
    '''
    
    _asset_path = None
    
    _ASSET_FOLDER_ = "assets"

    def __init__(self):
        '''
        Constructor
        '''

        self._asset_path = os.path.join(ProjectUtils.get_project_root() , AssetManager._ASSET_FOLDER_)

        if not os.path.exists(self._asset_path):
            raise RuntimeError("Missing assets folder.  Please check to make sure you have a /assets directory.")
    
    def get_asset_path(self, filename):
        "Get asset path."
        if os.path.exists(self._asset_path + "/" + filename):
            return self._asset_path + "/" + filename
        else:
            raise AssetNotFoundError("Cannot find asset: {0}".format(filename))


class AssetNotFoundError(RuntimeError):
    "raised when asset cannot be located."
    pass


WTF_ASSET_MANAGER = AssetManager()