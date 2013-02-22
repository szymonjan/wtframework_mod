'''
Created on Jan 28, 2013

@author: "David Lai"
'''

from wtframework.wtf.config.ConfigReader import WTF_CONFIG_READER
from wtframework.wtf.web.PageObject import PageObject

class PageFactory():
    "Page Factory class."

    @staticmethod
    def create_page(webdriver, page_obj_class, config_reader=WTF_CONFIG_READER):
        #Import moved inside to avoid circular import 
        from wtframework.wtf.web.PageObject import InvalidPageError
        
        """
        Instantiate a page object from a given Interface or Abstract class.
        
        Instantiating a Page from PageObject class usage:
            my_page_instance = PageFactory.create_page(webdriver, MyPageClass)
        
        Instantiating a Page from an Interface or base class
            import pages.mysite.* 
            my_page_instance = PageFactory.create_page(webdriver, MyPageAbstractBaseClass)
        
        Note: It'll only be able to detect pages that are imported.  To it's best to 
        do an import of all pages implementing a base class or the interface inside the 
        __init__.py of the package directory.  
        
        @param webdriver: Webdriver
        @type webdriver: WebDriver
        @param  page_obj_class: Class, AbstractBaseClass, or Interface to attempt to consturct.
        """
        # Walk through all classes of this sub class 
        subclasses = PageFactory.__itersubclasses(page_obj_class)

        current_matched_page = None
        for pageClass in subclasses :
            try:
                page = pageClass(webdriver, config_reader)
                if current_matched_page == None or page > current_matched_page:
                    current_matched_page = page
            except InvalidPageError:
                pass #This happens when the page fails check.
            except TypeError:
                pass #this happens when it tries to instantiate the original abstract class.
            except Exception as e:
                #Unexpected exception.
                raise e

        # Try the original class passed in if the subclasses didn't work.
        try:
            page = page_obj_class(webdriver, config_reader)
            if current_matched_page == None or page > current_matched_page:
                current_matched_page = page
        except InvalidPageError:
            pass #This happens when the page fails check.
        except TypeError:
            pass #this happens when it tries to instantiate the original abstract class.
        except Exception as e:
            #Unexpected exception.
            raise e

        # If no matching classes.
        if not isinstance(current_matched_page, PageObject):
            raise NoMatchingPageError("There's, no matching classes to this page. URL:%s" \
                                      % webdriver.current_url)
        else:
            return current_matched_page

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
