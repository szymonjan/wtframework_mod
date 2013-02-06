Wiredrive Web Test Framework
======
https://github.com/wiredrive/WD-WTF


Wiredrive Web Test Framework (referred to as WTF for short) provides a 
structured testing framework for testing a Web Application using nose unit 
test framework and Selenium Webdriver. 


Install
=======

Installation via PYPI

	pip install wiredrive-wtf


Setting up your project
=======================

Run the following command to initialize an empty project structure for a WTF test.
	
	wtf_init.py YourProjectName

Next you'll need to setup your python path.

	export PYTHONPATH=$PYTHONPATH:path/to/project/tests
	
Now the directory structure and your python path is setup so nosetests can run tests 
you write in the WTF framework.


Running your tests
==================

Run your tests using nosetests.

	./runtests.py


WTF Framework Features
======================

PageObjects
-----------


Configurable Tests
------------------



Credits
------------
David Lai