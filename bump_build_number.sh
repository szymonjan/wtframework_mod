#!/bin/sh

## This script is just a handle shell script I use to keep the WTF version numbers 
## in sync between version number in the framework, and the version number used in 
## the chrome extension, and the version number used in the setup tools.

echo "subsituting: $1 with $2"

sed s/$1/$2/ setup.py > setup.pie && mv setup.pie setup.py
sed s/$1/$2/ wtframework/__init__.py > init.pie && mv init.pie wtframework/__init__.py
sed s/$1/$2/ browser-plugins/chrome/wtf_page_mapper/manifest.json > manifest.jason && mv manifest.jason browser-plugins/chrome/wtf_page_mapper/manifest.json