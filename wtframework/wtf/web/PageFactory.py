'''
Created on Jan 28, 2013

@author: "David Lai"
'''
from wtframework.wtf.web.PageObject import InvalidPageError

class PageFactory():
    "Page Factory class."


    @staticmethod
    def create_page(webdriver, super_class):
        """
        Instantiate a page object from a given Interface or Abstract class.
        @param webdriver: Webdriver
        @type webdriver: WebDriver
        """
        # Walk through all classes of this sub class 
        subclasses = PageFactory.__itersubclasses(super_class)

        for pageClass in subclasses :
            try:
                page = pageClass(webdriver)
                return page;
            except InvalidPageError:
                pass #This happens when the page fails check.
            except TypeError:
                pass #this happens when it tries to instantiate the original abstract class.

        # Try the original class passed in if the subclasses didn't work.
        try:
            page = super_class(webdriver)
            return page;
        except InvalidPageError:
            pass #This happens when the page fails check.
        except TypeError:
            pass #this happens when it tries to instantiate the original abstract class.

        # If no matching classes.
        raise NoMatchingPageError("There's, no matching classes to this page. URL:%s" % webdriver.current_url)

    @staticmethod
    def __itersubclasses(cls, _seen=None):
        """
        Credit goes to: http://code.activestate.com/recipes/576949-find-all-subclasses-of-a-given-class/
        
        itersubclasses(cls)
    
        Generator over all subclasses of a given class, in depth first order.
    
        >>> list(itersubclasses(int)) == [bool]
        True
        >>> class A(object): pass
        >>> class B(A): pass
        >>> class C(A): pass
        >>> class D(B,C): pass
        >>> class E(D): pass
        >>> 
        >>> for cls in itersubclasses(A):
        ...     print(cls.__name__)
        B
        D
        E
        C
        >>> # get ALL (new-style) classes currently defined
        >>> [cls.__name__ for cls in itersubclasses(object)] #doctest: +ELLIPSIS
        ['type', ...'tuple', ...]
        """
        
        if not isinstance(cls, type):
            raise TypeError('itersubclasses must be called with '
                            'new-style classes, not %.100r' % cls)
        if _seen is None: _seen = set()
        try:
            subs = cls.__subclasses__()
        except TypeError: # fails only when cls is type
            subs = cls.__subclasses__(cls)
        for sub in subs:
            if sub not in _seen:
                _seen.add(sub)
                yield sub
                for sub in PageFactory.__itersubclasses(sub, _seen):
                    yield sub



class NoMatchingPageError(RuntimeError):
    "Raised when no matching page object is not found."
