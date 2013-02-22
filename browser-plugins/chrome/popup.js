//init scripts
SyntaxHighlighter.all();

//Track our current url when we open the extension popup window.
var currentUrl = "N/A";
chrome.tabs.getSelected(null,function(tab) {
	currentUrl = tab.url;
});


// Generate source code for Page Object.
function generatePageObjectCode() {
	var pageName = $("#wtf-page-name-input").val();

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

	
	$("#wtf-page-name-input").change(function() {
		console.log("page name changed");
		var newCode = '<script type="syntaxhighlighter" class="brush: python;"><![CDATA[\n\n' 
			+ generatePageObjectCode() + '\n\n]]></script>';
		
		$("#page-object-preview").empty();
		$("#page-object-preview").html(newCode);
		SyntaxHighlighter.highlight();
	});

	//Format the data URL right before the user clicks on the download link.
	$("#download-link").click(function() {

		var code = generatePageObjectCode();
		console.log(code);
		var url = "data:text/plain," + encodeURIComponent(code);
		$("#download-link").attr("href", url);
		
		
		//chrome.tabs.create({url: url});
	});
	
});



