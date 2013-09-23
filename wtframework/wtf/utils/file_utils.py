##########################################################################
#This file is part of WTFramework. 
#
#    WTFramework is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    WTFramework is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with WTFramework.  If not, see <http://www.gnu.org/licenses/>.
##########################################################################
import re
"""
This module contains functions for working with files.
"""

import os
import tempfile
from wtframework.wtf.utils.data_utils import generate_timestamped_string
import urllib


def temp_path(file_name=None):
    """
    Gets a temp path.
    
    Kwargs:
        file_name (str) : if file name is specified, it gets appended to the temp dir.
    
    Usage::
    
        temp_file_path = temp_path("myfile")
        copyfile("myfile", temp_file_path) # copies 'myfile' to '/tmp/myfile'

    """

    if file_name is None:
        file_name = generate_timestamped_string("wtf_temp_file")
    
    return os.path.join(tempfile.gettempdir(), file_name)



def create_temp_file(file_name=None, string_or_another_file = ""):
    """
    Creates a temp file using a given name.  Temp files are placed in the Project/temp/ 
    directory.  Any temp files being created with an existing temp file, will be 
    overridden.  This is useful for testing uploads, where you would want to create a 
    temporary file with a desired name, upload it, then delete the file when you're 
    done.

    Kwargs:
        file_name (str): Name of file
        string_or_another_file: Contents to set this file to. If this is set to a file, 
                                it will copy that file.  If this is set to a string, then 
                                it will write this string to the temp file.
    
    Return: 
        str - Returns the file path to the generated temp file.

    Usage::
    
        temp_file_path = create_temp_file("mytestfile", "The nimble fox jumps over the lazy dog.")
        file_obj = open(temp_file_path)
        os.remove(temp_file_path)

    """
    temp_file_path = temp_path(file_name)
    temp_file = open(temp_file_path, "w+")
    
    try: #attempt to read it as a file.
        original_file = string_or_another_file
        temp_file.write(original_file.read())
        
    except: #handle as a string type if we can't handle as a file.
        file_contents = string_or_another_file
        temp_file.write(file_contents)

    temp_file.close()
    return temp_file_path


def download_to_tempfile(url, file_name=None, extension=None):
    """
    Downloads a URL contents to a tempfile.  This is useful for testing downloads.
    It will download the contents of a URL to a tempfile, which you then can 
    open and use to validate the downloaded contents.
    
    Args:
        url (str) : URL of the contents to download.
    
    Kwargs:
        file_name (str): Name of file.
        extension (str): Extension to use.
    
    Return:
        str - Returns path to the temp file.

    """
    
    if not file_name:
        file_name = generate_timestamped_string("wtf_temp_file")
    
    if extension:
        file_path = temp_path(file_name + extension)
    else:
        ext = ""
        try:
            ext = re.search("\\.\\w+$", file_name).group(0)
        except:
            pass
        file_path = temp_path(file_name + ext)

    webFile = urllib.urlopen(url)
    localFile = open(file_path, 'w')
    localFile.write(webFile.read())
    webFile.close()
    localFile.close()

    return file_path

