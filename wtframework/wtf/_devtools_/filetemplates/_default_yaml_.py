contents = """
#########################################################################
# WTF Settings file.  Specify settings using yaml format.
# ex:
# login_settings: 
#   login: testuser
#   password: s3cure
#
# Then in your test code, you can refer to it using ConfigReader.
# 
# my_username = WTF_CONFIG_READER.get('login_settings.login')
# my_password = WTF_CONFIG_READER.get('login_settings.password')
# 
#########################################################################

# Settings for Selenium WebDriver used for browser testing.
selenium:
  # Set type to LOCAL for running locally, and to REMOTE, to run on a remote 
  # webdriver.  Default is LOCAL
  type: LOCAL
  #type: REMOTE

  # Terminate Selenium after all tests have run. Disabling this can be helpful
  # during debugging.  In operation you normally want to keep this to clean up 
  # after tests.
  shutdown_hook: true

  # Set to true, to reuse the same browser.  Set to false, to use a fresh browser 
  # instance each time.  If set to a number, this  would determine whether the browser 
  # session should be discarded after a certain time peroid.  
  # Default is 'true'
  reusebrowser: true

  # Take screenshot of browser on error.
  take_screenshot: true
  # Take reference screenshot upon encountering a new page.
  take_reference_screenshot: true

  # remote_url is required if type=REMOTE.  Set this to point at the Remote Webdriver 
  # connection string.
  #remote_url: http://url.to.seleniumgrid:4444/wd/hub

  # Browser can be the following options.
  # ANDROID, CHROME, FIREFOX, HTMLUNIT, HTMLUNITWITHJS, 
  # INTERNETEXPLORER, IPAD, IPHONE, OPERA, SAFARI
  browser: FIREFOX

  # Required if browser is set to CROME.  This should point to the chrome driver path 
  # relative to root '/'.
  #chromedriver_path: /Users/username/path/to/chromedriver

  # Path of Selenium server Jar file.  This is needed for Safari Driver.
  #selenium_server_path: /path/to/selenium-server-standalone-2.37.0.jar

  # Desired capabilities to pass to Selenium Grid.
  # Required if using selenium Grid.
  desired_capabilities:
    # Target browser version.
    #version: 22

    # ANY, ANDROID, LINUX, MAC, UNIX, VISTA, WIN7, WIN8, WINDOWS, XP
    platform: WINDOWS
    
    # Name you'd like to label your sessions. (useful for labeling on sauce)
    name: YourTestProjectName




# Default wait timeout settings. Timeout settings are specified in seconds.
timeout:
  # Timeout for quick things that would normally not need any sort of interstitial.
  brief: 5
  # Timeout for something short like a typical ajax response.
  short: 10
  # Timeout for something like loading a large page.
  normal: 30
  # Timeout for something considerably long, such waiting for something to process.
  long: 60
  # Timeout for something extremely long, which a user would normally get up and take a break.
  epic: 300


"""