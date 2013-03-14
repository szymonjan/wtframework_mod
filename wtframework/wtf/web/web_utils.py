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
from urllib2 import urlopen
import urllib2



class WebUtils(object):


    @staticmethod
    def check_url(url):
        '''
        Check if resource at URL is fetchable. (by trying to fetch it and checking for 200 status.
        @param url: Url to check.
        @type url: str
        @return: Returns a tuple of {success, response code}
        @rtype: Tuple
        '''
        request = urllib2.Request(url)
        try:
            response = urlopen(request)
            return True, response.code
        except urllib2.HTTPError as e:
            return False, e.code

    @staticmethod
    def is_webdriver_mobile(webdriver):
        "Check if a web driver if mobile."
        browser = webdriver.capabilities['browserName']

        if browser == u'iPhone' or \
        browser == u'android':
            return True
        else:
            return False

    @staticmethod
    def is_webdriver_ios(webdriver):
        "Check if a web driver if mobile."
        browser = webdriver.capabilities['browserName']

        if browser == u'iPhone' or \
        browser == u'iPad':
            return True
        else:
            return False



