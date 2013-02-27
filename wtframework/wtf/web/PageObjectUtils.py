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
Created on Jan 3, 2013

@author: "David Lai"
'''

class PageObjectUtils():
    '''
    Offers utility methods for PageObjects.
    '''

    @staticmethod
    def check_css_selectors(webdriver, *selectors):
        """
        Returns true if all CSS selectors passed in is found.  This can be used 
        to quickly validate a page
        @param webdriver: WebDriver.
        @type webdriver: WebDriver 
        @param *selectors: CSS selector for element to look for.
        @type *selectors: str
        """
        for selector in selectors:
            try:
                webdriver.find_element_by_css_selector(selector)
            except:
                return False # A selector failed.
        
        return True # All selectors succeeded