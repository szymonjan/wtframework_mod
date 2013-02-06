'''
Created on Dec 21, 2012

@author: "David Lai"
'''
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class WDDesiredCapabilities(DesiredCapabilities):
    '''
    Extending Selenium's Desired Capabilities to support additional browsers we 
    can access through Sauce Labs and other Selenium Grid sources we have access to.
    '''

    SAFARI = {"browserName": "safari",
                        "version": "",
                        "platform": "ANY",
                        "javascriptEnabled": True }

