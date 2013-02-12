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
