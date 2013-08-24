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

from wtframework.wtf.utils.project_utils import ProjectUtils
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
        """
        Get the full system path of a tiven asset if it exists.  Otherwise it throws 
        an error.
        
        Args:
            filename (str) - File name of a file in /assets folder to fetch the path for.
        
        Returns:
            str - path to the target file.
        
        Raises:
            AssetNotFoundError - if asset does not exist in the asset folder.
        
        Usage::
            path = WTF_ASSET_MANAGER.get_asset_path("my_asset.png")
            # path = /your/workspace/location/WTFProjectName/assets/my_asset.png 

        """
        if os.path.exists(self._asset_path + "/" + filename):
            return self._asset_path + "/" + filename
        else:
            raise AssetNotFoundError("Cannot find asset: {0}".format(filename))


class AssetNotFoundError(RuntimeError):
    "raised when asset cannot be located."
    pass

## Create Default instance of AssetManager ##
WTF_ASSET_MANAGER = AssetManager()
"""
Global instance of AssetManager

Usage Example::

    image_file_location = WTF_ASSET_MANAGER.get_asset_path("testimage.png")

"""
