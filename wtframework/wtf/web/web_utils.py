##########################################################################
#This file is part of WTFramework. 
#
#    WTFramework is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    WTFramework is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with WTFramework.  If not, see <http://www.gnu.org/licenses/>.
##########################################################################
from datetime import datetime, timedelta
from threading import Thread
from urllib2 import urlopen
from wtframework.wtf.config import WTF_TIMEOUT_MANAGER
from wtframework.wtf.utils.test_utils import do_and_ignore
from wtframework.wtf.web.page import PageFactory
from wtframework.wtf.web.webdriver import WTF_WEBDRIVER_MANAGER
import re
import time
import urllib2


class WebUtils(object):
    "Utility class for web testing."


    @staticmethod
    def check_url(url):
        '''
        Check if resource at URL is fetchable. (by trying to fetch it and checking for 200 status.
        
        Args:
            url (str): Url to check.
        
        Returns:
            Returns a tuple of {True/False, response code}

        '''
        request = urllib2.Request(url)
        try:
            response = urlopen(request)
            return True, response.code
        except urllib2.HTTPError as e:
            return False, e.code

    @staticmethod
    def get_base_url(webdriver):
        """
        Get the current base URL.
        
        Args:
            webdriver: Selenium webdriver.
        
        Returns:
            str - base URL. 
        
        usage::
        
            WebUtils.get_base_url("http://www.google.com/?q=blah")
            #returns 'http://www.google.com'

        """
        current_url = webdriver.current_url
        try:
            return re.findall("^[^/]+//[^/$]+", current_url)[0]
        except:
            raise RuntimeError("Unable to process base url: {0}".format(current_url) )


    @staticmethod
    def is_webdriver_mobile(webdriver):
        """
        Check if a web driver if mobile.
        
        Args:
            webdriver (WebDriver): Selenium webdriver.

        """
        browser = webdriver.capabilities['browserName']

        if browser == u'iPhone' or \
        browser == u'android':
            return True
        else:
            return False

    @staticmethod
    def is_webdriver_ios(webdriver):
        """
        Check if a web driver if mobile.
        
        Args:
            webdriver (WebDriver): Selenium webdriver.

        """
        browser = webdriver.capabilities['browserName']

        if browser == u'iPhone' or \
        browser == u'iPad':
            return True
        else:
            return False


    @staticmethod
    def switch_to_window(page_class, webdriver):
        """
        Utility method for switching between windows.  It will search through currently open 
        windows, then switch to the window matching the provided PageObject class.
        
        Args:
            page_class (PageObject): Page class to search for/instantiate.
            webdriver (WebDriver): Selenium webdriver.

        usage::

            WebUtils.switch_to_window(DetailsPopUpPage, driver) # switches to the pop up window.

        """
        window_list = list(webdriver.window_handles)
        original_window = webdriver.current_window_handle
        for window_handle in window_list:
            webdriver.switch_to_window(window_handle)
            try:
                return PageFactory.create_page(page_class, webdriver)
            except:
                pass
        
        webdriver.switch_to_window(original_window)
        raise WindowNotFoundError("Window {0} not found.")


class BrowserStandBy(object):
    """
    This class allows you to put a browser on stand by sending no-op commands to keep 
    a selenium grid session from timing out.  This is useful for running tests on 
    3rd party grids that have short timeouts.

    Usage::

        stand_by = BrowserStandBy().start()
        check_email_received() # some operation that can take a long time.
        stand_by.stop()


    """
    
    def __init__(self, webdriver=None, max_time=WTF_TIMEOUT_MANAGER.EPIC, sleep=5, **kwargs):
        """
        Constructor

        Kwargs:
            webdriver (WebDriver) - Selenium Webdriver instance
            max_time (number) - Maximum wait time to keep the browser on stand by.
            sleep (number) - Number of seconds to wait between sending heart beats.

        """
        if webdriver is None:
            webdriver = WTF_WEBDRIVER_MANAGER.get_driver()

        self.webdriver = webdriver
        self._sleep_time = sleep
        self._max_time = max_time

        self._autostart = False
        try:
            if kwargs['_autostart']:
                self._autostart = True
        except KeyError:
            pass


    @classmethod
    def start_standby(cls, webdriver=None, max_time=WTF_TIMEOUT_MANAGER.EPIC, sleep=5):
        """
        Create an instance of BrowserStandBy() and immediately return a running instance.
        
        This is best used in a 'with' block.
        
        Example::

            with BrowserStandBy.start_standby():
                # Now browser is in standby, you can do a bunch of stuff with in this block.
                # ...
            
            # We are now outside the block, and the browser standby has ended.

        """
        return cls(webdriver=webdriver, max_time=max_time, sleep=sleep, _autostart=True)


    def start(self):
        """
        Start standing by.  A periodic command like 'current_url' will be sent to the 
        webdriver instance to prevent it from timing out.

        """
        self._end_time = datetime.now() + timedelta(seconds = self._max_time)
        self._thread = Thread(target=lambda: self.__stand_by_loop())
        self._keep_running = True
        self._thread.start()
        return self


    def stop(self):
        """
        Stop BrowserStandBy from sending additional calls to webdriver.
        
        """
        self._keep_running = False
        return self


    def __stand_by_loop(self):
        print self._keep_running
        while datetime.now() < self._end_time and self._keep_running:
            self.webdriver.current_url #Just performing current_url to keep this alive.
            time.sleep(self._sleep_time)

    def __del__(self):
        do_and_ignore(lambda: self.stop())
        self._thread = None


    def __enter__(self):
        if self._autostart:
            self.start()
        return self

    def __exit__(self, type_, value, traceback):
        # Stop standby on exit
        do_and_ignore(lambda: self.stop())


class WindowNotFoundError(RuntimeError):
    "Raised when window is not found by web_utils script."


