'''
Created on Jan 31, 2013

@author: "David Lai"
'''
from datetime import datetime
import random
import string

class DataUtils():
    
    @staticmethod
    def generate_timestamped_string(subject, number_of_random_chars=4):
        """
        Generate time-stamped string. Format as follows...
        2013-01-31_14:12:23_SubjectString_a3Zg
        @param subject: String to use as subject.
        @type subject: str
        """
        random_str = ''.join(random.choice(string.ascii_letters) \
                             for _ in range(number_of_random_chars))
        fmt = '%Y-%m-%d_%H.%M.%S_{subject}_{random_str}'
        ts_string = datetime.now().strftime(fmt).\
            format(subject=subject, random_str=random_str)
        return ts_string