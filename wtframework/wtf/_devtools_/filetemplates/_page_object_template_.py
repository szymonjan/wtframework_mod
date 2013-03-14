content = \
'''
"""
Created on {date}

"""
from wtframework.wtf.web.page import PageObject, InvalidPageError


class {pagename}(PageObject):
    """
    Page object for {url}
    """
    
    # Identifying properties #
    _partial_url = "{partialurl}"
    
    ######### Object Map ###########
    
{objectmap}
    
    ################################
    
    def _validate_page(self, webdriver):
        "@see: PageObject"
        # Validating page by url
        current_url = webdriver.current_url
        if not {pagename}._partial_url in current_url:
            raise InvalidPageError("Page does not match {pagename}. Current Url:".format(current_url)) 
        
    
    #### Define your PageObject Actions Below #####
    
    
    #END Class
'''