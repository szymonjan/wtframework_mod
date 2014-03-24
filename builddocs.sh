#!/bin/sh

## This is just a handy shell script created for generating the code docs
## locally.  This is essentially what will be run by readthedocs.org
## on their side when it runs Build tasks to generate code docs.

set PYTHONPATH=$PWD
cd docs
make html
cd ..