content=\
'''

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
'''