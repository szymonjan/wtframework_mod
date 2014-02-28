
import abc


class ISearchPage(object):

    """
    Example of how you can use a an interface to create a higher level 
    abstraction that can be used by PageFactory.
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

# Import your sub-pages implementing the interface in the
# so PageFactory will know about which subclasses of this
# interface exists.
import tests.pages.www_google_com  # @UnusedImport
import tests.pages.www_yahoo_com  # @UnusedImport
