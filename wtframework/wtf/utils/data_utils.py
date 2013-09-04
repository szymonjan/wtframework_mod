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
"""
The purpose of this module is to provide functions for generating data that 
can be used in tests.
"""
from datetime import datetime
import random
import string


def generate_timestamped_string(subject="test", number_of_random_chars=4):
    """
    Generate time-stamped string. Format as follows...
    
    `2013-01-31_14:12:23_SubjectString_a3Zg`
    
    
    Kwargs:
        subject (str): String to use as subject.
        number_of_random_chars (int) : Number of random characters to append.


    This method is helpful for creating unique names with timestamps in them so 
    when you have to troubleshoot an issue, the name is easier to find.::
    
        self.project_name = generate_timestamped_string("project")
        new_project_page.create_project(project_name)

    """
    random_str = generate_random_string(number_of_random_chars)
    timestamp = generate_timestamp()
    return "{timestamp}_{subject}_{random_str}".format(timestamp=timestamp, 
                                                       subject=subject,
                                                        random_str=random_str)


def generate_timestamp(date_format="%Y-%m-%d_%H.%M.%S"):
    """
    Returns timestamped string. '2012-03-15_14:42:23
    
    Kwargs:
        format: A date/time format string.  If not specified, the default will be used.

    """
    return datetime.now().strftime(date_format);


def generate_random_string(number_of_random_chars=8, character_set=string.ascii_letters):
    """
    Generate a series of random characters.
    
    Kwargs:
        number_of_random_chars (int) : Number of characters long
        character_set (str): Specify a character set.  Default is ASCII
    """
    return ''.join(random.choice(character_set) \
            for _ in range(number_of_random_chars))

