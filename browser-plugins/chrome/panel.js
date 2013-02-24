

//Track our current url when we open the extension popup window.
var currentUrl = "N/A";
chrome.tabs.getSelected(null,function(tab) {
	currentUrl = tab.url;
});


// Generate source code for Page Object.
function generatePageObjectCode() {
	var pageName = $("#wtf-page-name-input").val();
	if (pageName == undefined || pageName == "") {
		pageName = "MyPage";
	}
	
	//generate text for our page object.
	var code = [];
	code.push(
"'''",
"Created on " + (new Date()).toString(),
"",
"@author:Your Name Here" ,
"'''",
"from wtframework.wtf.web.PageObject import PageObject, InvalidPageError",
"from tests.pages.ISearchPage import ISearchPage",
"",
"",
"class " + pageName + "(PageObject, ISearchPage):",
"    '''",
"    " + pageName,
"    PageObject representing a page like:",
"    " + currentUrl ,
"    '''",
"",
"",
"    def _validate_page(self, webdriver)",
"    '''",
"    Validates we are on the correct page.",
"    '''",
""
	);
	return code.join("\n");
}


//on document ready
$(document).ready(function() {
	//load initial content.
	var newCode = '<script type="syntaxhighlighter" class="brush: python;"><![CDATA[\n\n' 
		+ generatePageObjectCode() + '\n\n]]></script>';
	$("#page-object-preview").empty();
	$("#page-object-preview").html(newCode);
	SyntaxHighlighter.highlight();
	
	//Change page name handler.
	$("#wtf-page-name-input").change(function() {
		//Validate Page Name
		var namePattern = /^[A-Z][a-z0-9]*([A-Z][a-z0-9]*)*$/;
		if (!namePattern.test($("#wtf-page-name-input").val())) {
			$("#page-name-section").addClass("has-errors");
			return;
		} else {
			$("#page-name-section").removeClass("has-errors");
		}
		
		console.log("page name changed");
		var newCode = '<script type="syntaxhighlighter" class="brush: python;"><![CDATA[\n\n' 
			+ generatePageObjectCode() + '\n\n]]></script>';
		
		$("#page-object-preview").empty();
		$("#page-object-preview").html(newCode);
		SyntaxHighlighter.highlight();
		
		console.log("css:" + $("#wtf-page-name-input").getCssPath());
		console.log("xpath:" + $("#wtf-page-name-input").getXPath());
	});

	//Format the data URL for the PageObject download.
	$("#download-link").click(function() {

		var code = generatePageObjectCode();
		console.log(code);
		var url = "data:text/plain," + encodeURIComponent(code);
		
		var pageName = $("#wtf-page-name-input").val();
		if (pageName == undefined || pageName == "") {
			pageName = "MyPage";
		}

		var filename = pageName + ".py";
		$("#download-link").attr("href", url);
		$("#download-link").attr("download", filename);
	});
	
});


// Credit for this goes to 
// http://stackoverflow.com/questions/5706837/get-unique-selector-of-element-in-jquery
jQuery.fn.extend({
    getCssPath: function () {
        var path, node = this;
        while (node.length) {
            var realNode = node[0], name = realNode.localName;
            if (!name) break;
            name = name.toLowerCase();

            var parent = node.parent();

            var sameTagSiblings = parent.children(name);
            if (sameTagSiblings.length > 1) { 
                allSiblings = parent.children();
                var index = allSiblings.index(realNode) + 1;
                if (index > 1) {
                    name += ':nth-child(' + index + ')';
                }
            }

            path = name + (path ? '>' + path : '');
            node = parent;
        }

        return path;
    }
});

// Credit for this goes to 
// http://stackoverflow.com/questions/8446175/a-jquery-script-to-find-xpath-location-of-clicked-element
jQuery.fn.extend({
    getXPath: function () {
        var element = this[0];
        var xpath = '';
        for ( ; element && element.nodeType == 1; element = element.parentNode )
        {
            var id = $(element.parentNode).children(element.tagName).index(element) + 1;
            id > 1 ? (id = '[' + id + ']') : (id = '');
            xpath = '/' + element.tagName.toLowerCase() + id + xpath;
        }
        return xpath;
	}

});