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

from datetime import datetime
import random
import string


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