WTF - Web Test Framework
======
https://github.com/wiredrive/wtframework

Selenium does a good job at providing APIs for automating the browser.  What the Web Test 
Framework (referred to as WTF for short) is to take that base, and build on it to provide 
a structured test framework for testing a Web Applications in a maintainable manner.  The 
goal is to provide the project structures and tools to help QA/SDET professionals quickly 
setup and develop acceptance level web tests which are configurable, robust, and easy to 
use.  The ultimate goal is to build a common framework on top of Selenium to provide test 
professionals the tools to build web tests as easily as how Rails and Django makes it easy
to build web applications.


Installation
=======

Requirements
*	Python 2.7 - http://www.python.org/download/
*	PyPi (pip) - http://www.pip-installer.org/en/latest/

Installation via PYPI

	pip install wtframework


Setting up your project
=======================

Run the following command to initialize an empty project structure for a WTF test.
	
	wtf_init.py YourProjectName --withexamples

Windows Note: .py files may not be executable, you may have to prefix these commands 
with the python command. 
	python wtf_init.py YourProject --withexamples
	
This will create an the folders and packages of your project.  You'll see something like:

	/YourProjectName
		/assets - place non-code files used in your tests here.
		/configs - location of config files.
		/data - data files (like CSV files) goes here.
		/reference-screenshots - if enabled, reference screenshots are placed here.
		/reports - test result XML files will go here when you run tests.
		/screenshots - screenshots taken on test failures will go here.
		/tests - top level package for your test code.
			/flows - high level reuseable multipage flows.
			/models - data models go here. (like DataBase ORM code)
			/pages - Your page objects go here.
			/support - reuseable support utility functions go here.
			/testdata - custom code for working with test data.
			/tests - Your high level tests will go here.
	
	
Now the directory structure and your python path is setup so nosetests can run tests 
you write in the WTF framework.


Configuring Eclipse/PyDev Environment
-------------------------------------
1.	Download/Install Eclipse. http://www.eclipse.org/
2.	Install the PyDev plugin. http://pydev.org/
3.	Goto Eclipse -> Preferences (Or on windows, this Window -> Preferences )
4.	Goto PyDev -> Interpretor Python then open the Libraries tab.
5.	Add you python site-packages (where pip installs packages to)
	At this point your PyDev enviornment should be able to recognize your 
	installed packages.
6.	In Eclipse,  goto "File" and create a new PyDev project.
7.	Fill out the required fields and use your generated project structure as
	your Project folder.  This should create the PyDev project files necessary to
	allow you to work on this project as a PyDev project.
8.  Open the project settings, then under "PyDev - PYTHONPATH" settings, add 
    your project base directory as a source folder.  Then save.

At this point, you should be able to right click, select "Run As" and execute your test 
cases as PyUnit test case.


Installing the WTF PageObject Utility Chrome Extension
------------------------------------------------------
1. Download or clone the source.  The extension source code is included under 
   `/browser-plugins` directory.
2. Open Chrome.
3. Open the Chrome's Preferences menu, and select "Extensions"
4. Enable the "Developer mode" checkbox.
5. Click on the "Load unpack extension..." button.
6. Then select the "chrome" folder under the 'wtframework/browser-plugins/' directory.
7. At this point the plugin should be installed.  You can test out the plugin by going 
   to another webpage, clicking on the `WTF` extension button in your chrome toolbar, 
   this should open the WTF PageObject Utility window.

Running your tests
==================

Run your tests using nosetests.

	./runtests.py [-c ConfigFile]

This will execute the unit tests in the `tests/tests` folder.  The test results will be
written to `reports/`, any screenshots taken during errors will be stored in the
`screenshots/` folder.


WTF Framework Features
======================

PageObjects & Chrome Extension
------------------------------
PageObjects is a common strategy for Selenium Webdriver programmers to create self 
contained PageObjects to encapsulate the low level UI details from their high level 
tests.  This allows changes in pages to be maintained in their separate page objects 
so tests that use the page, need not worry about the details.

WTF provides handy chrome plugin to help you create page objects.  See Chrome plugin 
installation instructions above.  The chrome plugin will help you quickly generate the 
boiler-plate code, some simple validate methods, and help with the tedious task of 
mapping the WebElements on this page.

![Image](/docs/images/WTF_panel_parts.png?raw=true)


To Create a page object, do the following:

1. Go to your target page.  Then click the WTF toolbar button, then select "Scan Page"
2. A popup window will open.  You'll be presented with a form that'll include fields for 
   naming your PageObject, setting the page verification method, and a button to map 
   your page elements.  
3. Fill in an appropriate name for your page object.
4. Adjust the page verification characteristics.  You may want to change it from a string 
   compare to a regular expression and replace variable parameters with wildcards.
5. Map the elements you want to include. To map an element, first click on the button 
   labled `Map New Element`.  You'll be taken back to your page window, dismiss the 
   pop-up dialog, then click on the element you wish to map.  After clicking on the 
   element, you'll notice a new entry will be created in your PageObject Utility window.
   Fill in the fields and adjust the object identification properties.  If the 
   identification properties in the fields do not match an element on the page, the fields
   will turn red.  Fix these before moving on.
6. A code preview will be displayed at the bottom part of this window.  Review what's 
   there before downloading.
7. Click on the "Download" link that's right above the Preview area.  This will allow you 
   to download this file.  Save this file to your `YourProject/tests/pages` directory.
8. Edit this file in a code editor and add whatever high level method calls you want to 
   expose.  Then you'll have a fully functioning page object.


You can now use this page object you created like this:

	from wtframework.wtf.web.pages import PageFactory
	from pages.homepage import HomePage
	...
	homepage = PageFactory.create_page(HomePage)
	homepage.login(username, password) # you will need to implement this part.

Alternatively, you can use the WebUtils to wait for the page to load.  This will allow 
you to specify a timeout period (in seconds) to wait for this page to finish loading.

	from wtframework.wtf.web.pages import PageUtils
	...
	slow_loading_page = PageUtils.wait_until_page_loaded(YourPageClass, 60)

Note: This will use the PageObject's `_validate_page()` to check if the page is 
matching the expected page.  It's good to not use a web element in addition to URL or 
title validation, that way the page validation does not happen until page content appears 
on the screen.

Once you have created a PageOjbect, you'll want to go in and edit the file and make any 
changes to the mappings and page verification routines.  As a good practice, it's good 
to write methods to expose your transactional logic as a higher level method call 
to avoid cluttering your high level tests and test flows with low level UI logic.

See: http://engineeringquality.blogspot.com/2012/12/python-quick-and-dirty-pageobject.html


Configurable Tests
------------------
Being able to run tests across different environments and settings is a powerful tool.
WTF has a powerful tool for working with configurations called `WTF_CONFIG_READER`.  By 
default, it'll look at the default.yaml file in the /configs directory.  But you may 
specify using other config files by setting the `WTF_ENV` variable.  This is useful to 
have different config files for your different test environments.  Then in your CI 
system, you can just specify which config file to use.

In your tests, you can pull the values you have stored in your config file using the 
`WTF_CONFIG_READER` like this:

	base_url = WTF_CONFIG_READER.get_value("baseurl")
	webdriver.get( base_url + "/somelocation" )

This allows you to make your test environment agnostic, runnable across multiple 
configurations with just a switch of an environment variable.  This is good for storing 
environment settings and locations, account information (like DB login), connection 
strings, etc... 
	

WTFBaseTest
-----------
WTF framework adds some functionality to Python's unittest that are helpful for more end 
to end level tests.  In order to leverage this functionality, your tests should extend 
the `WTFBaseTest` base class.  

WTFBaseTest comes with a ScreenCaptureTestWatcher.  You may also implement your own 
test watcher by extending `TestWatcher` class, and overriding it's methods.  This is 
useful for creating your own base test with your own actions such as recording results 
to Test Case Management upon test completion.  If you like to do without the added 
functionality of WTFBaseTest, you can use `WatchedTestCase` and extend it.


Data Driven Testing
-------------------
WTF framework provides a easy way of doing Data-Driven-Tests using CSV files.  Data 
files are stored in the `data/` folder, and can be easily accessed using the utility 
class `WTF_DATA_MANAGER.get_data_file("nameOfCsvFile")`.  You can iterate a single test 
over those CSV row values by using the `@ddt` and `@csvdata` decorators.

You can have a csv file with first row the column headers like, `data/animals.csv'

	Animal,Type,Size
	Dog,Mammal,3.0
	Cat,Mammal,1.5
	Lizzard,Reptile,2.0

Then in `your_data_driven_test.py`, you can reference these values as follows:

	# Use @ddt decorator at the class level.
	@ddt
	class TestCsvDataDrivenTest(TestCase):
    
    	# Then use the @csvdata decorator to flag a test method data driven.
    	@csvdata("testdata.csv")
	    def test_csv_datadriven(self, parameter_dic):
	    	#Then in your test, you can use the parameter passed into your test
	    	# as a dictionary with key corresponding to your CSV headers.
	    	animal = parameter_dic['Animal']
	    	type = parameter_dic['Type']
	    	size = parameter_dict['Size']
	    	...


Misc
====

License
-------
This framework is free and open source.  Licensed under GPLv3. See 'LICENSE.TXT' for 
license details.

How to Contribute
-----------------
You can fork this repository.  To get the unit tests not marked as skipped running, 
you'll need to edit or supply your own config file with values for the selenium settings.

Development on this project is currently done using NVIE branching model.  
http://nvie.com/posts/a-successful-git-branching-model/

To submit code changes, please submit pull requests against the development branch. 

See here for other ways you can help.
[https://github.com/wiredrive/wtframework/wiki/How-you-can-help.]

Credits
------------
David Lai <david@wiredrive.com>