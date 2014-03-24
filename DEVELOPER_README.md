
Getting UnitTests to work on your local machine.
====
There are a few dependencies needed to get all unit tests working locally in your dev 
environment, most of them configurations settings and setting up the browsers needed 
for the tests to run.

1.  Install Firefox (real browser tests will use this browser by default)
2.  Download a copy of Selenium Server .jar file, http://docs.seleniumhq.org/download/
    and copy it to a known directory that's accessible.
3.  Install PhantomJS, http://phantomjs.org/
4.  Create a copy of `/wtframework/configs/default.yaml`, and fill in all the needed 
    configuration settings, especially ones for PhantomJS, which is used by headless 
    tests.  Then set your `WTF_ENV=yourconfig` (minus the .yaml) to point to your 
    config.
   

Release Process 
====
(Note: this is meant for the release engineer handling the release)
The release process is somewhat manual at the moment.  One day we may try to fully 
automate it via Travis, but for now we do the following steps.

1.  Using GitFlow, https://github.com/nvie/gitflow, start a release branch.  This will be 
	where we'll do any final staging, version number bumps and last minute bug fixes.
2.  Bump the version numbers, use the `./bump_build_number.sh oldver newversion` this 
	will replace the version numbers on all the files that contain the current version 
	numbers in the project.
3.	If any examples (files under `/tests/`) were updated it.  Run the following command 
	to update the template generation script. `python generate_examples.py`.  This will 
	take the files under `/tests/` and compile them into template strings that can be 
	used by the framework's `wtf_init.py` script.
4.  Create a source distribution of the framework, `python setup.py sdist`.  This will 
	create a tarball with the framework in the `/dist/` folder.
5.	Install the framework and do any additional testing. 
	`pip install dist/wtframework-version#.tar`.
6.	Publish the framework to PyPi.org. `python setup sdist upload`.  You may need to 
	register your ssh keys or enter a username/password if this is your first time 
	publishing.
7.	Finish the current release using GitFlow.  This will automatically merge the release 
	into master and any bug fix changes back into develop.  Then push to origin so the 
	source is available on GitHub.
8. 	Publish the code docs.  Login to ReadTheDocs.org, select the WTFramework project, 
	then click navigate to Builds.  In the Builds page, click on the Build button and 
	select "latest".
