'''
Created on Dec 13, 2012

@author: david
'''
from wtframework.wtf.utils.ProjectUtils import ProjectUtils
import os
import re
import yaml


class ConfigReader:
    '''
    Config Reader provides a singleton instance of ConfigReader for looking up 
    values for config variables.
    '''

    CONFIG_LOCATION = 'configs/'
    DEFAULT_CONFIG_FILE = 'default'
    CONFIG_EXT = '.yaml'

    ENV_VARS = "WTF_ENV"

    _dataMaps = None #instance variable to store config data loaded.
    _singleton_instance = None #class variable to track singleton.

    def __init__(self, _env_var_ = None):
        self._dataMaps = []

        #load default yaml file if this is not a unit test.
        try:
            if _env_var_ != None: 
                # We pass in a custom env var for unit testing.
                configs = re.split(",|;", _env_var_)
                for config in reversed(configs):
                    self.__load_config_file(config)
            elif os.environ[ConfigReader.ENV_VARS] == None:
                raise Exception("No Config Specified, using defaults.")
            else:
                # Read and load in all configs specified in reverse order
                configs = re.split(",|;", str(os.environ[ConfigReader.ENV_VARS]))
                for config in reversed(configs):
                    self.__load_config_file(config)
        except Exception as e:
            #Fall back to default.yaml file when no config settings are specified.
            print e
            self.__load_config_file(ConfigReader.DEFAULT_CONFIG_FILE)


    def get_value(self,key):
        '''
        Gets the value from the yaml config based on the key.
        
        No type casting is performed, any type casting should be 
        performed by the caller.
        
        @param key: Name of the config you wish to retrieve.  
        @type key: str
        '''
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

        raise KeyError("Key '{0}' does not exist".format(key))

    def get_value_or_default(self,key, default):
        '''
        @param key: Name of the config you with to retrieve.
        @type key: str
        @param default: Default value to return if they key/value is not specified
            in the config.
        '''
        try:
            return self.get_value(key)
        except KeyError:
            return default

    def __load_config_file(self, file_name):
        config_file_location = os.path.join(ProjectUtils.get_project_root() +
                                            ConfigReader.CONFIG_LOCATION + 
                                            file_name + 
                                            ConfigReader.CONFIG_EXT)
        config_yaml = open(config_file_location, 'r')
        dataMap = yaml.load(config_yaml)
        self._dataMaps.insert(0, dataMap)
        config_yaml.close()



class ConfigReaderAccessException(Exception):
    '''
    Exception Thrown that should be explicitly caught when trying to 
    manually set the config reader.
    '''
    pass


# Create a global constant for referencing this to avoid re-instantiating 
# this object over and over.
WTF_CONFIG_READER = ConfigReader()