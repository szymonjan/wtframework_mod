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
from wtframework.wtf.config import WTF_CONFIG_READER

# The idea of a 'testdata' package is to organize your test data and test settings.
# While tests can reference the WTF_CONFIG_READER directly like this
#
#    admin_user = WTF_CONFIG_READER.get("admin_user", "admin")
#
# But you'll have the same hard coded "admin_user" string all over your tests.
# It is better to abstract that away into function calls so the same hard coded 
# string isn't repeated throughout your code.  This creates a single point of 
# maintenance for any config refactoring.
#
#
# This is an example of how you can uses a settings object.
# Here in your test, you can now refer to your admin login 
# like this
#
#     login_page.login( get_admin_user(), get_test_admin_password() )
#
# Then when you run on different envionrments or different accounts,
# you can simply pass in a config file that'll specify the value for 
# 'admin_user' and 'admin_password'
def get_admin_user():
    return WTF_CONFIG_READER.get("admin_user", "admin")

def get_admin_password():
    return WTF_CONFIG_READER.get("admin_password", "password")


def get_search_provider():
    "Configure this via the 'search_provider' setting."
    return WTF_CONFIG_READER.get("search_provider", "http://www.google.com")