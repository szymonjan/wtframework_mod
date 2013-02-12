#!/usr/bin/env python
'''
Created on Feb 4, 2013

@author: "David Lai"
'''
from optparse import OptionParser
from wtframework.wtf._devtools_.filetemplates import _default_yaml_, \
    _root_folder_placeholder_, _runtests_py_, _TestExample_py_, _ISearchPage_py_,\
    _GoogleSearchPage_py_, _YahooSearchPage_py_
import os.path


################# UTILITY METHODS ######################

def ensure_dir(dir_path): 
    if not os.path.exists(dir_path):
        print "Creating {0}".format(dir_path)
        os.makedirs(dir_path)
    else: 
        print "{0} already exists".format(dir_path)

def create_file(filepath, contents):
    if not os.path.exists(filepath):
        print "Creating {0}".format(filepath)
        text_file = open(filepath, "w")
        text_file.write(contents)
        text_file.close()
    else:
        print "{0} already exists.".format(filepath)

################# MAIN SETUP SCRIPT ######################
if __name__ == '__main__':
        
    usage = "usage: %prog NameOfProject [--withexamples]"
    parser = OptionParser(usage=usage)
    parser.add_option("--withexamples", action="store_true",
                      default=False, dest="examples",
                      help="Include example web test.")

    (options, args) = parser.parse_args()
    print options
    print args
    if len(args) != 1:
        parser.error("wrong number of arguments")
    project_dir = os.getcwd() + "/" + args[0]
    ensure_dir(project_dir)
    
    #create folder root file
    create_file(project_dir + "/.wtf_root_folder", _root_folder_placeholder_.contents)
    #create runtest script.
    create_file(project_dir + "/runtests.py", _runtests_py_.content)
    # make file executable
    os.chmod(project_dir + "/runtests.py", 0755)
    
    #create asset folder
    ensure_dir(project_dir + "/assets")

    #create asset folder
    ensure_dir(project_dir + "/data")
    
    #create configs
    ensure_dir(project_dir + "/configs")
    #create default config file
    create_file(project_dir + "/configs/default.yaml", _default_yaml_.contents)
    
    #create reference screenshots dir.
    ensure_dir(project_dir + "/reference-screenshots")
    
    #create reports dir
    ensure_dir(project_dir + "/reports")
    
    #create screenshots dir
    ensure_dir(project_dir + "/screenshots")
    
    #create tests dir
    ensure_dir(project_dir + "/tests")
    create_file(project_dir + "/tests/__init__.py", "'Top level tests folder.  Organize your items in the subfolders below.'")
    ensure_dir(project_dir + "/tests/flows")
    create_file(project_dir + "/tests/flows/__init__.py", "'Put reusable multi-page flows here.'")
    ensure_dir(project_dir + "/tests/models")
    create_file(project_dir + "/tests/models/__init__.py", "'Put models like database abstractions here.'")
    ensure_dir(project_dir + "/tests/pages")
    create_file(project_dir + "/tests/pages/__init__.py", "'Put your PageObjects here.'")
    ensure_dir(project_dir + "/tests/support")
    create_file(project_dir + "/tests/support/__init__.py", "Put various utility functions you want to reuse here.'")
    ensure_dir(project_dir + "/tests/testdata")
    create_file(project_dir + "/tests/testdata/__init__.py", "'Put reuseable functions for generating and handling test data here.'")
    ensure_dir(project_dir + "/tests/tests")
    create_file(project_dir + "/tests/tests/__init__.py", "'Put your high level tests here.'")


    if options.examples == True:
        print "Generating example files."
        create_file(project_dir + "/tests/tests/TestExample.py", _TestExample_py_.content)
        create_file(project_dir + "/tests/pages/ISearchPage.py", _ISearchPage_py_.content)
        create_file(project_dir + "/tests/pages/GoogleSearchPage.py", _GoogleSearchPage_py_.content)
        create_file(project_dir + "/tests/pages/YahooSearchPage.py", _YahooSearchPage_py_.content)
        



