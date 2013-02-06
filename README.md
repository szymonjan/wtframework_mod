WTF - Web Test Framework
======
https://github.com/wiredrive/wtframework


Wiredrive Web Test Framework (referred to as WTF for short) provides a 
structured testing framework for testing a Web Application using nose unit 
test framework and Selenium Webdriver. 


Install
=======

Installation via PYPI

	pip install wtframework


Setting up your project
=======================

Run the following command to initialize an empty project structure for a WTF test.
	
	wtf_init.py YourProjectName

Next you'll need to setup your python path.

	export PYTHONPATH=$PYTHONPATH:path/to/project/tests
	
Now the directory structure and your python path is setup so nosetests can run tests 
you write in the WTF framework.


Configuring Eclipse/PyDev Environment
-------------------------------------
1. Download/Install Eclipse. http://www.eclipse.org/
2. Install the PyDev plugin. http://pydev.org/
3. Goto Eclipse -> Preferences (Or on windows, this Window -> Preferences )
4. Goto PyDev -> Interpretor Python then open the Libraries tab.
5. Add you python site-packages (where pip installs packages to)
At this point your PyDev enviornment should be able to recognize your 
installed packages.
6. In Eclipse,  goto "File" and create a new PyDev project.
7. Fill out the required fields and use your generated project structure as
your Project folder.  This should create the PyDev project files necessary to
allow you to work on this project as a PyDev project.


Running your tests
==================

Run your tests using nosetests.

	./runtests.py



WTF Framework Features
======================

PageObjects
-----------
#TODO

Configurable Tests
------------------
#TODO


Credits
------------
David Lai <david@wiredrive.com>