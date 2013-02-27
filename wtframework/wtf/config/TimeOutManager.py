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
Created on Dec 21, 2012

@author: "David Lai"
'''
from wtframework.wtf.config.ConfigReader import WTF_CONFIG_READER

class TimeOutManager(object):
    """
    Utility class for reading timeout values from config.
    """
    _config = None
    
    def __init__(self):
        "Initializer"
        self._config = WTF_CONFIG_READER

    @property
    def BRIEF(self):
        return self._config.get_value_or_default("timeout.brief", 5)

    @property
    def SHORT(self):
        return self._config.get_value_or_default("timeout.short", 15)


    @property
    def NORMAL(self):
        return self._config.get_value_or_default("timeout.normal", 30)

    @property
    def LONG(self):
        return self._config.get_value_or_default("timeout.long", 60)

    @property
    def EPIC(self):
        return self._config.get_value_or_default("timeout.epic", 300)



# Create a global constant for referencing this to avoid re-instantiating 
# this object over and over.
WTF_TIMEOUT_MANAGER = TimeOutManager()