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

from tests.pages.search_page import ISearchPage
from wtframework.wtf.web.page import PageFactory


# You can use flow functions to group together a set of calls you make frequently 
# so you can reuse them between tests.

def perform_search(search_term, webdriver):
    """
    This flow function groups together a navigation to the search page, and 
    a search.
    """
    webdriver.get("http://www.google.com")
    search_page = PageFactory.create_page(ISearchPage, webdriver)
    search_page.search(search_term)

    return search_page