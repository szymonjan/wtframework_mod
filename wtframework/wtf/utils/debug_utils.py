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
from __future__ import print_function
from datetime import datetime
from wtframework.wtf.config import WTF_CONFIG_READER
import inspect

"""
The purpose of this class is to provide tools for helping debug WTF tests.
"""

class TimeDebugger(object):
    "Object to keeps track of time and has utility methods to print it"
    

    def start_timer(self):
        """
        Start the timer.
        """
        self.start_time = datetime.now()


    def print_time(self, message="Time is now: ", print_frame_info=True):
        """
        Print the current elapsed time.
        
        Kwargs:
            message (str) : Message to prefix the time stamp.
            print_frame_info (bool) : Add frame info to the print message.

        """
        if print_frame_info:
            frame_info = inspect.getouterframes(inspect.currentframe())[1]
            print(message, (datetime.now() - self.start_time), frame_info)
        else:
            print(message, (datetime.now() - self.start_time))


    def get_split(self):
        """
        Returns the current ellapsed time.
        
        Returns:
            timedelta - current ellapsed time.
        """
        return (datetime.now() - self.start_time)


def print_debug(*args, **kwargs):
    """
    Print if and only if the debug flag is set true in the config.yaml file.
    
    Args:
        args : var args of print arguments.

    """
    if WTF_CONFIG_READER.get("debug", False) == True:
        print(*args, **kwargs)
