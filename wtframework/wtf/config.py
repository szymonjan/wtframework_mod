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


from types import NoneType
from wtframework.wtf.utils.project_utils import ProjectUtils
import os
import re
import yaml
import time


class ConfigReader:
    '''
    Config Reader provides a way of reading configuration settings. 
    '''

    CONFIG_LOCATION = 'configs/'
    DEFAULT_CONFIG_FILE = 'default'
    CONFIG_EXT = '.yaml'

    ENV_VARS = "WTF_ENV"
    ENV_PREFIX = "WTF_"

    _dataMaps = None #instance variable to store config data loaded.
    _singleton_instance = None #class variable to track singleton.

    def __init__(self, _env_var_ = None):
        """
        constructor
        """
        self._dataMaps = []

        #load default yaml file if this is not a unit test.
        try:
            if _env_var_ != None: 
                # We pass in a custom env var for unit testing.
                configs = re.split(",|;", _env_var_)
                for config in reversed(configs):
                    self.__load_config_file(config)
            elif not ConfigReader.ENV_VARS in os.environ:
                print "Config file not specified.  Using config/defaults.yaml"
                self.__load_config_file(ConfigReader.DEFAULT_CONFIG_FILE)
            else:
                # Read and load in all configs specified in reverse order
                configs = re.split(",|;", str(os.environ[ConfigReader.ENV_VARS]))
                for config in reversed(configs):
                    self.__load_config_file(config)

                
        except Exception as e:
            #Fall back to default.yaml file when no config settings are specified.
            print "An error occurred while loading config file:", e
            raise e
            


    class __NoDefaultSpecified__(object):
        "No default specified to config reader."
        pass


    def get(self,key, default_value=__NoDefaultSpecified__):
        '''
        Gets the value from the yaml config based on the key.
        
        No type casting is performed, any type casting should be 
        performed by the caller.
        
        Args:
            key (str) - Config setting key.
        
        Kwargs:
            default_value - Default value to return if config is not specified.
        
        Returns:
            Returns value stored in config file.

        '''
        # First attempt to get the var from OS enviornment.
        os_env_string = ConfigReader.ENV_PREFIX + key
        os_env_string = os_env_string.replace(".", "_")
        if type(os.getenv(os_env_string)) != NoneType:
            return os.getenv(os_env_string)

        # Otherwise search through config files.
        for data_map in self._dataMaps:
            try:
                if "." in key:
                    #this is a multi levl string
                    namespaces = key.split(".")
                    temp_var = data_map
                    for name in namespaces:
                        temp_var = temp_var[name]
                    return temp_var
                else:
                    value = data_map[key]
                    return value                
            except (AttributeError, TypeError, KeyError):
                pass
            
        if default_value == self.__NoDefaultSpecified__:
            raise KeyError("Key '{0}' does not exist".format(key))
        else:
            return default_value


    def __load_config_file(self, file_name):
        try:
            config_file_location = os.path.join(ProjectUtils.get_project_root() +
                                                ConfigReader.CONFIG_LOCATION + 
                                                file_name + 
                                                ConfigReader.CONFIG_EXT)
            print "locating config file:", config_file_location
            config_yaml = open(config_file_location, 'r')
            dataMap = yaml.load(config_yaml)
            self._dataMaps.insert(0, dataMap)
            config_yaml.close()
        except Exception as e:
            print "Error loading config file " + file_name
            raise ConfigFileReadError("Error reading config file " + file_name, e)


class ConfigFileReadError(RuntimeError):
    """
    Raised when a config file is not found.
    """
    pass




# Create a global constant for referencing this to avoid re-instantiating 
# this object over and over.
WTF_CONFIG_READER = ConfigReader()
"""
Global instance of ConfigReader

Usage::

    testurl = WTF_CONFIG_READER.get("testurl", default="http://www.example.com")

"""


class TimeOutManager(object):
    """
    Utility class for getting default config values for various timeout 
    periods.
    """
    _config = None
    
    def __init__(self, config_reader = None):
        """
        Constructor
        
        Args:
            config_reader (ConfigReader) - override default config reader.
        """
        if config_reader:
            self._config = config_reader
        else:
            self._config = WTF_CONFIG_READER

    @property
    def BRIEF(self):
        """
        Useful for waiting/pausing for things that should happen near instant.
        
        Returns:
            number - brief wait period.
        """
        return self._config.get("timeout.brief", 5)

    @property
    def SHORT(self):
        """"
        Useful for waiting/pausing for things that are just long enough for a
        typical ajax request to return.

        Returns:
            number - short wait period. 
        """
        return self._config.get("timeout.short", 10)


    @property
    def NORMAL(self):
        """
        Useful for a normal considerable wait.  Such as waiting for a large page to 
        fully load on screen.

        Returns:
            number - normal wait period.
        """
        return self._config.get("timeout.normal", 30)

    @property
    def LONG(self):
        """
        Useful for things that take a long time.  Such as waiting for an moderate size 
        download/upload to complete.

        Returns:
            number - long wait period.
        """
        return self._config.get("timeout.long", 60)

    @property
    def EPIC(self):
        """
        Useful for operations that take an extremly long amount of time.  For example, 
        waiting for a large upload to complete.

        Returns:
            number - epic wait period.
        """
        return self._config.get("timeout.epic", 300)


    def brief_pause(self):
        """
        Do a brief pause.
        """
        time.sleep(self.BRIEF)


    def short_pause(self):
        """
        Do a short pause.
        """
        time.sleep(self.SHORT)


    def normal_pause(self):
        """
        Do a normal pause.
        """
        time.sleep(self.NORMAL)


    def long_pause(self):
        """
        Do a long pause.
        """
        time.sleep(self.LONG)


    def epic_pause(self):
        """
        Do a epic pause.
        """
        time.sleep(self.EPIC)



WTF_TIMEOUT_MANAGER = TimeOutManager()
"""
Global instance of TimeOutManager

Usage Example::

    PageUtils.wait_for_page_to_load(SlowPage, WTF_TIMEOUT_MANAGER.LONG)


"""