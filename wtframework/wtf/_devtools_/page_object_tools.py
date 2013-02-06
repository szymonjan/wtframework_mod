'''
Created on Feb 6, 2013

@author: davidlai
'''
from wtframework.wtf._devtools_.filetemplates import _page_object_template_
from datetime import datetime
import re
import urllib2

def _process_input_tag(html):
    pass

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
    
    print "Creating object map for <input> tags..."
    for input_tag_match in input_tag_iter:
        obj_map_entry = _process_input_tag(input_tag_match.group(0))
        print input_tag_match.group(0)
    
    
    
    objectmap = "    "+ \
    "objectname = lambda self:self.webdriver.find_element_by_css('.hello')"+\
    "\n"
    
    
    
    return _page_object_template_.content.format(date=datetime.now(),
                                                url="http://www.google.com",
                                                pagename=page_name,
                                                partialurl=partial_url,
                                                objectmap=objectmap)