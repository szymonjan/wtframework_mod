'''
Created on Jan 2, 2013

@author: "David Lai"
'''
from datetime import datetime, timedelta
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from urllib2 import urlopen
from wtframework.wtf.config.TimeOutManager import TIMEOUT_MANAGER
from wtframework.wtf.web.PageFactory import PageFactory
import inspect
import time
import urllib2


class WebUtils(object):
    """
    Utility methods for working with web pages and web elements.
    """
    
    @staticmethod
    def wait_until_page_loaded(page_obj_class, webdriver, timeout=TIMEOUT_MANAGER.NORMAL, sleep=0.5):
        """
        Waits until the page is loaded.
        @return: Returns PageObject of type passed in.
        @rtype: PageObject
        """

        end_time = datetime.now() + timedelta(seconds = timeout)
        last_exception = None
        while datetime.now() < end_time:
            try:
                if inspect.isabstract(page_obj_class):
                    return PageFactory.create_page(webdriver, page_obj_class)
                else:
                    return page_obj_class(webdriver)
            except Exception as e:
                last_exception = e
                pass
            time.sleep(sleep)

        print "Unable to construct page, last exception", last_exception
        raise PageLoadTimeoutError("Timedout while waiting for {page} to load. Url:{url}".\
                              format(page=page_obj_class.__name__, url=webdriver.current_url))

    @staticmethod
    def wait_until_element_not_visible(webdriver, locator_lambda_expression, \
                                       timeout=TIMEOUT_MANAGER.NORMAL, sleep=0.5):
        "Wait for a WebElement to disappear."
        # Wait for loading progress indicator to go away.
        try:
            stoptime = datetime.now() + timedelta(seconds=timeout)
            while datetime.now() < stoptime:
                element = WebDriverWait(webdriver, TIMEOUT_MANAGER.BRIEF).until(locator_lambda_expression)
                if element.is_displayed():
                    time.sleep(sleep)
                else:
                    break
        except TimeoutException:
            pass

    @staticmethod
    def is_image_loaded(webdriver, webelement):
        '''
        Check if an image (in an image tag) is loaded.
        Note: This call will not work against background images.  Only Images in <img> tags.
        
        @param webelement: WebDriver web element to validate.
        @type webelement: WebElement
        '''
        script = "return arguments[0].complete && type of arguments[0].naturalWidth != \"undefined\" " +\
                 "&& arguments[0].naturalWidth > 0"
        try:
            return webdriver.execute_script(script, webelement)
        except:
            return False #Img Tag Element is not on page.

    @staticmethod
    def check_url(url):
        '''
        Check if resource at URL is fetchable. (by trying to fetch it and checking for 200 status.
        @param url: Url to check.
        @type url: str
        @return: Returns a tuple of {success, response code}
        @rtype: Tuple
        '''
        request = urllib2.Request(url)
        try:
            response = urlopen(request)
            return True, response.code
        except urllib2.HTTPError as e:
            return False, e.code

    @staticmethod
    def is_webdriver_mobile(webdriver):
        "Check if a web driver if mobile."
        browser = webdriver.capabilities['browserName']

        if browser == u'iPhone' or \
        browser == u'android':
            return True
        else:
            return False

    @staticmethod
    def is_webdriver_ios(webdriver):
        "Check if a web driver if mobile."
        browser = webdriver.capabilities['browserName']

        if browser == u'iPhone' or \
        browser == u'iPad':
            return True
        else:
            return False



##################################################################

class WebUtilOperationTimeoutError(Exception):
    "Timed out while waiting for a WebUtil action"

class PageLoadTimeoutError(WebUtilOperationTimeoutError):
    "Timeout while waiting for page to load."
