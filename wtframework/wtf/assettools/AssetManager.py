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