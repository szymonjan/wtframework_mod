
import abc


class ISearchPage(object):
    """
    Example of how you can use a mix-in as an interface.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def search(self, search_string):
        "Submit a search"
        pass
    
    @abc.abstractmethod
    def result_contains(self):
        "Submit a search"
        pass

# Import your subpages Implementing an Interface in the 
# "__init__.py" so PageFactory will know about it's existence.
import tests.pages.www_google_com #@UnusedImport
import tests.pages.www_yahoo_com #@UnusedImport
