content=\
'''

from tests.pages.search_page import ISearchPage
from wtframework.wtf.web.page import PageObject, InvalidPageError



# Extend PageObject to create a page object.  You can also use Mix-Ins 
# to implement interfaces to use with PageFactory.
class GoogleSearchPage(PageObject, ISearchPage):
    """
    Example Page Object Using Google.
    """
    
    # Object Mappings for fields on this page. #
    # Note the 'self.webdriver', this is because PageObjects keep track 
    # of their own webdriver that's driving the page.
    search_field = lambda self:self.webdriver.find_element_by_name('q')
    
    # Page objects all override the _validate_page() method so pages 
    # can self validate upon creation.
    def _validate_page(self, webdriver):
        "Check to make sure we're on google.com"
        if "google.com" not in webdriver.current_url:
            # Raise an InvalidPageError to let the PageFactory 
            # know that this isn't a page match.
            raise InvalidPageError("This is not google.")

    
    # Here we are implementing the Search method as defined by 
    # ISearchPage interface.
    def search(self, search_string):
        "Enter a search"
        
        # We can call a mapped element by calling it's lambda function.
        self.search_field().send_keys(search_string)
        

    # Here we are implementing the validate result contains method.
    def result_contains(self, text_to_check):
        "Simple check to see if the word occurs in the page."
        return text_to_check in self.webdriver.page_source
        

'''        