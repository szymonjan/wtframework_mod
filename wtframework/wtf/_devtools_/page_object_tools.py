'''
Created on Feb 6, 2013

@author: davidlai
'''
from datetime import datetime
from wtframework.wtf._devtools_.filetemplates import _page_object_template_
import re
import urllib2

def _process_input_tag(html):
    #find name property expression, used is varous input types.
    name_expr = "name=['\"]([^'\"]+)['\"]"
    
    # process text input
    if ("type=\"text\"" in html) or (not "type" in html):
        name = re.search(name_expr, html, re.IGNORECASE).group(1)
        obj = "input_{name} = lambda self: self.webdriver.find_element_by_name(\"{name}\")".format(name=name)
        return obj
    # process textarea inputs
    
    # process radio types
    # TODO
    
    # process checkbox types
    # TODO
    
    #process submit types.
    if "type=\"submit\"" in html:
        try:
            name = re.search(name_expr, html, re.IGNORECASE).group(1)
            obj = "input_{name} = lambda self: self.webdriver.find_element_by_name(\"{name}\")".format(name=name)
            return obj
        except:
            pass
        
        
    print "why here"
    

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