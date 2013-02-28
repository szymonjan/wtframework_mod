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
Created on Feb 1, 2013

@author: "David Lai"
'''

from datetime import datetime

class TimeDebug(object):
    "Object to keeps track of time and has utility methods to print it"
    

    def start_timer(self):
        self.start_time = datetime.now()

    def print_time(self, message="Time is now: "):
        print message, (datetime.now() - self.start_time)
        
    def get_split(self):
        return (datetime.now() - self.start_time)
