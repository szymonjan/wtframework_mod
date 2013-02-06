#!/usr/bin/env python
'''
Created on Feb 4, 2013

@author: "David Lai"
'''
from optparse import OptionParser
from wtframework.wtf._devtools_.filetemplates import _default_yaml_, \
    _root_folder_placeholder_, _runtests_py_
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
    ensure_dir(project_dir + "/tests/flows")
    ensure_dir(project_dir + "/tests/models")
    ensure_dir(project_dir + "/tests/pages")
    ensure_dir(project_dir + "/tests/support")
    ensure_dir(project_dir + "/tests/testdata")
    ensure_dir(project_dir + "/tests/tests")


    create_examples = False
    if options.examples == True:
        #Create additional project files.
        #TODO
        pass



