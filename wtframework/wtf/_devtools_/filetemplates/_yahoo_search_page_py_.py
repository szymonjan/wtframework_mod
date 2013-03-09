content=\
'''


from wtframework.wtf.web.page import PageObject, InvalidPageError
from tests.pages.search_page import ISearchPage

class YahooSearchPage(PageObject, ISearchPage):
    "Simple PageObject class"
    
    # Object Mappings for fields on this page. #
    # Note the 'self.webdriver', this is because PageObjects keep track 
    # of their own webdriver that's driving the page.
    search_field = lambda self:self.webdriver.find_element_by_name('p')
    submit_button = lambda self:self.webdriver.find_eleent_by_id('search-submit')
    
    # Page objects all override the _validate_page() method so pages 
    # can self validate upon creation.
    def _validate_page(self, webdriver):
        "Check to make sure we're on google.com"
        if "yahoo.com" not in webdriver.current_url:
            # Raise an InvalidPageError to let the PageFactory 
            # know that this isn't a page match.
            raise InvalidPageError("This is not Yahoo.")

    # Here we are implementing the Search method as defined by 
    # ISearchPage interface.
    def search(self, search_string):
        "Enter a search"
        
        # We can call a mapped element by calling it's lambda function.
        self.search_field().send_keys(search_string)
        self.submit_button().submit_button

    # Here we are implementing the validate result contains method.
    def result_contains(self, text_to_check):
        "Simple check to see if the word occurs in the page."
        return text_to_check in self.webdriver.page_source

'''
