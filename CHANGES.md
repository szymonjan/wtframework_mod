## v0.4.2
- Embed exceptions raised in wait_until()
- Create screenshots directory if not exists at the time of screen capture.
- Fixes to the project generator scripts.

## v0.4.1
- Changes to make library python 2/3 compatible.  Many underhood changes to logging and 
  string handling.
- Ensure screenshots directory exists before trying to save screenshots.

## v0.4.0
- Convert all strings to use unicode.  You can now use unicode data within your tests
  now.

## v0.3.12
- Log the node info of the remote webdriver if possible. (to help debugging)
- Copy desired capabilities to prevent any unintended side effects.

## v0.3.11
- Fixed screenshot capture for non-unix systems. (thanks Hellspam)

## v0.3.10
- Resolve merge issues in v0.3.9

## v0.3.9
- Added ability to specify messages to various timeout errors.
- Log warning instead of halting the test if Safari window cannot be maximized.

## v0.3.8
- Added support for local Safari Driver

## v0.3.7
- Stop casting all desired capabilities settings to strings. (only browser version)

## v0.3.6
- Added support for passing executable path config for PhantomJS driver.
- Added ignore ssl error flag to PhantomJS driver startup

## v0.3.5
- Added more code examples.
- Reworked how example files are generated.

## v0.3.4
- Restored `WTF_WEBDRIVER_MANAGER` shut down hook.

## v0.3.3
- Remove duplicate instance of data_utils to avoid confusion.
- Updated documentation

## v0.3.2
- Fix `is_driver_available()`
- Modified WatchedTestCase to always run tearDown() when setup() fails. (Note: this is 
different behavior than the standard unittest, however this type of behavior is descired 
for end-to-end tests) 

## v0.3.1
- WebdriverManager support for multi-threaded tests 
- Flatten out desired capabilities for multi-level keys (support browserstack settings)

## v0.3.0 
- Switched to using nosetest2 as the test runner
- Switched to using unittest2 instead of unittest for the WatchedTestCase class base.
- WTFramework project is now tested by Travis-CI, 
  https://travis-ci.org/wiredrive/wtframework

## v0.2.22-3 - 6/28/2013
- new_driver() can now take an optional test name parameter.  This is useful for passing 
test names into Sauce on demand.
- ConfigReader will now throw errors instead of falling back to default for an invalid 
config file.

## v0.2.16-21 - 6/26/2013
- Added support for using a fresh browser instance for each test
- Added BrowserStandBy utility class
- Use `new_driver()` instead of `get_driver()` for creating new drivers.
- Avoid instantiation drivers in keyword args
- Moved driver cleanup into WebdriverManager from WebdriverFactory
- WebdriverManager.close_driver() for manually quitting a driver.

## v0.2.14-15 - 6/20/2013
- Added CI builds to open source project
- Added reading config variable from OS environment.  Name your variables, WTF_VARNAME

## v0.2.13 - 6/4/2013
- Add raw search to imap emails.

## v0.2.12 - 5/24/2013
- Remove NoseXUnit dependency

## v0.2.11 - 5/24/2013
- Added various utility functions.
- Added --version to command line utils.

## v0.2.10 - 5/6/2013
- Minor enhancements

## v0.2.9 - 4/22/2013
- Minor changes to aid in debugging.

## v0.2.8 - 4/02/2013
- Fixes to email search

## v0.2.7 - 4/02/2013
- Added a couple utility methods.

## v0.2.6 - 3/29/2013
- Added utils for working with temp files.
- Moved wiki screenshots out of this project.
- Allow allow wait for page method to accept a single bad page class without passing it 
  in a list.

## v0.2.5 - 3/25/2013
- Improve logging around webdriver factory.
- By default use Firefox webdriver if no settings provided.
- Fix typo in chrome plugin generated pageobject code.

## v0.2.4 - 3/25/2013
- Fix bug in 'do_until()' function.

## v0.2.3 - 3/22/2013
- New Feature: chrome plugin has a "check" button to highlight target element on the page.
- Fixed issue with using lists of classes for `wait_until_page_loaded()`.
- Fixed issue in chrome plugin with getting element name of elements mapped initially 
with CSS


## v0.2.2 Bug fix. 3/18/2013
- Fixed issues in name spacing in the 'email' module.

## v0.2.1 Minor tweaks. 3/15/2013
- Improved the string output for delayed test failure to make it easier to read.
- Fixed a minor bug with delayed test failure.
- Truncate screenshot file names to 20 characters to prevent files becoming too long.

## v0.2.0 Major refactor to bring naming in line with python standards. 3/14/2013
- Refactored module, classes, and variable naming in line with python standards.
- PageFactory now supports lists of classes.
- Added more unit tests.
- Fixed screenshot on error file names.

##v0.1.1-0.1.4
- Bug fixes to Python generated code from plugin.
- Added ability to manually map an element in chrome plugin.
- Add screenshot to readme

##v0.1.0
- Added support for delayed test failure.  This allows you to perform an assert, 
  but not fail the test until the end so you can test multiple items before the 
  test fails.
- Initial release of the Chrome PageObject tool for WTF. 

##v0.0.12 Minor bug fixes 2/12/2013
- Removed some bad imports that interfered with running webdriver off the grid.

##v0.0.11 Test Watchers and Data-Driven-Tests 2/12/2013
- Added TestWatcher feature for registering test watcher to your test cases.
- Refactored WTFBaseTest implementation to use TestWatcher
- Added CSV data driven test support
- Under the hood refactoring.

##v0.0.10 Changes to generator 2/8/2013
- added '-c configfile' option to runtests.py for specifying config file.
- added more input type support for page object generator.
- minor bug fixes.

##v0.0.8 Changes to generator 2/6/2013
- Added 'generate-test' option for wtf_tools
- Added some documentation.

##v0.0.6 Refactoring 2/6/2013
- Added .create_page() method to base PageObject.  Simple shortcut for calling PageFactory

##v0.0.5 Refactoring 2/6/2013
- Changed some constants around.
- WebDriverProvider is now WebDriverManager

##v0.1.1, 2013/2/3 -- Initial Release
