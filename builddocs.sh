#!/bin/sh

set PYTHONPATH=$PWD
cd docs
make html
cd ..