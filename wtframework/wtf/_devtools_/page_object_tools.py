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

from datetime import datetime
from wtframework.wtf._devtools_.filetemplates import _page_object_template_
import re
import urllib2

def _process_input_tag(html):
    html = html.lower()

    #find name property expression, used is varous input types.
    name_expr = "name=['\"]([^'\"]+)['\"]"
    value_expr = "value=['\"]([^'\"]+)['\"]"
    
    # process text input
    if ("type=\"text\"" in html) or (not "type" in html):
        try:
            name = re.search(name_expr, html, re.IGNORECASE).group(1)
            display_name = _strip_non_chars_from_name(name)
            obj = "{name}_text = lambda self: self.webdriver.find_element_by_name(\"{name}\")".format(name=name, display_name=display_name)
            return obj
        except:
            pass

    # process password input
    if ("type=\"password\"" in html):
        try:
            name = re.search(name_expr, html, re.IGNORECASE).group(1)
            display_name = _strip_non_chars_from_name(name)
            if display_name != "password": 
                display_name += "_password"
            obj = "{display_name} = lambda self: self.webdriver.find_element_by_name(\"{name}\")".format(name=name, display_name=display_name)
            return obj
        except:
            pass
        
    # process textarea inputs
    if ("<textarea" in html):
        try:
            name = re.search(name_expr, html, re.IGNORECASE).group(1)
            display_name = _strip_non_chars_from_name(name)
            obj = "{name}_textarea = lambda self: self.webdriver.find_element_by_name(\"{name}\")".format(name=name, display_name=display_name)
            
            return obj
        except:
            pass
    
    # process radio types
    if ("type=\"radio\"" in html):
        try:
            name = re.search(name_expr, html, re.IGNORECASE).group(1)
            value = re.search(value_expr, html, re.IGNORECASE).group(1)
            display_name = _strip_non_chars_from_name(name + "_" + value)
            obj = "{display_name}_radio = lambda self: self.webdriver.find_element_by_css_selector(\"input[name='{name}'][value='{value}']\")".format(name=name, display_name=display_name, value=value)
            
            return obj
        except:
            pass

    
    # process checkbox types
    if ("type=\"checkbox\"" in html):
        try:
            name = re.search(name_expr, html, re.IGNORECASE).group(1)
            value = re.search(value_expr, html, re.IGNORECASE).group(1)
            display_name = _strip_non_chars_from_name(name + "_" + value)
            obj = "{display_name}_checkbox = lambda self: self.webdriver.find_element_by_css_selector(\"input[name='{name}'][value='{value}']\")".format(name=name, display_name=display_name, value=value)
            
            return obj
        except:
            pass
    
    #process submit types.
    if "type=\"submit\"" in html:
        try:
            try:
                name = re.search(name_expr, html, re.IGNORECASE).group(1)
                display_name = _strip_non_chars_from_name(name)
                obj = "{display_name}_submit_button = lambda self: self.webdriver.find_element_by_name(\"{name}\")".format(name=name, display_name=display_name)
                return obj
            except:
                value = re.search(value_expr, html, re.IGNORECASE).group(1)
                display_name = _strip_non_chars_from_name(value)
                obj = "{display_name}_submit_button = lambda self: self.webdriver.find_element_by_css_selector(\"input[type='submit'][value='{value}'\")".format(value=value, display_name=display_name)
                return obj
        except:
            pass

    #process button types.
    if "type=\"button\"" in html:
        try:
            try:
                name = re.search(name_expr, html, re.IGNORECASE).group(1)
                display_name = _strip_non_chars_from_name(name)
                obj = "{display_name}_submit_button = lambda self: self.webdriver.find_element_by_name(\"{name}\")".format(name=name, display_name=display_name)
                return obj
            except:
                value = re.search(value_expr, html, re.IGNORECASE).group(1)
                display_name = _strip_non_chars_from_name(value)
                obj = "{display_name}_submit_button = lambda self: self.webdriver.find_element_by_css_selector(\"input[type='submit'][value='{value}'\")".format(value=value, display_name=display_name)
                return obj
        except:
            pass
    

def _strip_non_chars_from_name(name):
    "remove non alpha chars from name."
    return re.sub("[^a-zA-Z_]", "_", name).lower()

def generate_page_object(page_name, url):
    "Generate page object from URL"
    
    # Attempt to extract partial URL for verification.
    url_with_path = r'^.*//[^/]+([^?]+)?|$'
    try:
        match = re.match(url_with_path, url)
        partial_url = match.group(1)
        print "Using partial URL for location verification. ", partial_url
    except:
        #use full url since we couldn't extract a partial.
        partial_url = url
        print "Could not find useable partial url, using full url.", url
    
    #Attempt to map input objects.
    print "Processing page source..."
    response = urllib2.urlopen(url)
    html = response.read()
    input_tags_expr = r'<\s*input[^>]*>'
    input_tag_iter = re.finditer(input_tags_expr, html, re.IGNORECASE)
    
    objectmap = ""
    print "Creating object map for <input> tags..."
    for input_tag_match in input_tag_iter:
        if not "hidden" in input_tag_match.group(0):
            try:
                print "processing" + input_tag_match.group(0)
                obj_map_entry = _process_input_tag(input_tag_match.group(0))
                objectmap += "    " + obj_map_entry +"\n"
            except Exception as e:
                print e
                # we failed to process it, nothing more we can do.
                pass 
    
    return _page_object_template_.content.format(date=datetime.now(),
                                                url=url,
                                                pagename=page_name,
                                                partialurl=partial_url,
                                                objectmap=objectmap)