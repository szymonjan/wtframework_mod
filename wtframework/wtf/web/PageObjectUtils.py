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