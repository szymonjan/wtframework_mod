'''
Created on Dec 21, 2012

@author: "David Lai"
'''
from wtframework.wtf.config.ConfigReader import CONFIG_READER

class TimeOutManager(object):
    """
    Utility class for reading timeout values from config.
    """
    _config = None
    
    def __init__(self):
        "Initializer"
        self._config = CONFIG_READER

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
TIMEOUT_MANAGER = TimeOutManager()