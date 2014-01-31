##########################################################################
# This file is part of WTFramework. 
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

from wtframework.wtf._devtools_.filetemplates import _test_template_


def generate_empty_test(test_name):
    "Generates an empty test extending WTFBaseTest"
    date = datetime.now()
    return _test_template_.contents.format(date=date, testname=test_name)
