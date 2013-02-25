// Store my tab id so I can use it to refocus on this window.
var myTabId = null;

//Track our current url when we open the extension popup window.
var currentTab = null;
var currentUrl = "N/A";
var currentTitle = "";
var pageName = "MyPageObjectPage";
var itemsUsingRegEx = [];

var useUrlValidation = true;
var urlValidationType = "substring";
var urlValidationFilter = currentUrl;

var useTitleValidation = false;
var titleValidationType = "substring";
var titleValidationFilter = currentTitle;


//parse out currentUrl of host page.
var getParams = location.search.substr(location.search.indexOf("?")+1);

currentTab = chrome.tabs.get(parseInt(getParams), function(tab) {
	currentTab = tab;
	currentUrl = urlValidationFilter = tab.url;
	currentTitle = titleValidationFilter = tab.title;
	
	$("#wtf-validate-by-url-text").val(tab.url);
	$("#wtf-validate-by-title-text").val(tab.title);
	
	//Initial PageObj view.
	refreshPageObjectPreview();
});
console.log("Url:" + currentUrl);

chrome.extension.onMessage.addListener(
		function(request, sender, sendResponse) {
			// Return if message is not passed by WTFramework.
			if (request.wtframework != true)
				return;
			
			
			// Handle the popup sending us the tab URL upon initializing this window.
			if (request.action == "tabUrl") {
				currentUrl = request.tabUrl;
				console.log("URL received. " + request.tabUrl);				
				refreshPageObjectPreview();				
				sendResponse({response: "OK"});
			}
			
			if (request.action == "element-mapped") {
				// TODO: handle incoming mapped elements from content scripts.
				console.log("receive element mapping request");
				console.log(request);
				
				//Refocus on this window.
				chrome.tabs.update(myTabId, {active:true}, function(tab) {});
			}
			
});

// Generate source code for Page Object.
function generatePageObjectCode() {
	
	//generate text for our page object.
	var code = [];
	
	//Note: below code is purposely flushed left for easier reading of the spacing in the 
	// code that's getting generated. (which is important in python)
	
	//Preamble
	code.push(
"'''",
"Created on " + (new Date()).toString(),
"",
"@author:Your Name Here" ,
"'''",
"from wtframework.wtf.web.PageObject import PageObject, InvalidPageError"
	);
	//import regular expression if used.
	if (itemsUsingRegEx.length > 0) {
		code.push("import re");
	}
	
	code.push(	
"",
""
	);
	
	//Class Name
	code.push(
"class " + pageName + "(PageObject):",
"    '''",
"    " + pageName,
"    WTFramework PageObject representing a page like:",
"    " + currentUrl ,
"    '''",
"",
""
	);

	//Page Element mappings.
	code.push(
"    ### Page Elements Section ###"
	);
	//TODO: insert mapped elements.
	
	code.push(
"    ### End Page Elements Section ###",
"",
""
	);	
	
	
	
	//Validation code
	code.push(
"    def _validate_page(self, webdriver)",
"        '''",
"        Validates we are on the correct page.",
"        '''",
""
	);
	
	var pageValidationUsed = false; //track if any validation is used
	
	if(useUrlValidation) {
		console.log("handling url verification.")
		pageValidationUsed = true;
		if (urlValidationType == "substring") {
			code.push(
"        if not '" + urlValidationFilter + "' in webdriver.current_url:",
"            raise InvalidPageError(\"This page did not pass " + pageName + " page validation.\")",
""
					);
		} else if (urlValidationType == "regex") {
			code.push(
"        if not re.search('" + urlValidationFilter + "', webdriver.current_url):",
"            raise InvalidPageError(\"This page did not pass " + pageName + " page validation.\")",
""
					);
		}
	} 
	
	if(useTitleValidation) {
		console.log("handling title verification.")
		pageValidationUsed = true;
		if (titleValidationType == "substring") {
			code.push(
"        if not '" + titleValidationFilter + "' in webdriver.title:",
"            raise InvalidPageError(\"This page did not pass " + pageName + " page validation.\")",
""
					);
		} else if (titleValidationType == "regex") {
			code.push(
"        if not re.search('" + titleValidationFilter + "', webdriver.title):",
"            raise InvalidPageError(\"This page did not pass " + pageName + " page validation.\")",
""
					);
		}
	}
	
	if(!useUrlValidation && !useTitleValidation){
		code.push(
"        # Insert page validation code here.",
"        pass"					
		);
	}
	
	
	
	//Combine our lines into the generated file.
	code.push("\n");
	return code.join("\n");
} //END OF Generate PageObject code.


function addRegExUser(user) {
	if (itemsUsingRegEx.indexOf(user) < 0) {
		itemsUsingRegEx.push(user);
	}
}

function removeRegExUser(user) {
	if (itemsUsingRegEx.indexOf(user) >= 0) {
		var index = itemsUsingRegEx.indexOf(user);
		itemsUsingRegEx.splice(index, 1);
	}
}



function refreshPageObjectPreview() {
	var newCode = '<script type="syntaxhighlighter" class="brush: python;"><![CDATA[\n\n' 
		+ generatePageObjectCode() + '\n\n]]></script>';
	$("#page-object-preview").empty();
	$("#page-object-preview").html(newCode);
	SyntaxHighlighter.highlight();
}

//on document ready
$(document).ready(function() {

	
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
		pageName = $("#wtf-page-name-input").val();
		
		refreshPageObjectPreview();
	});

	//Format the data URL for the PageObject download.
	$("#download-link").click(function() {

		var code = generatePageObjectCode();
		console.log(code);
		var url = "data:text/plain," + encodeURIComponent(code);


		var filename = pageName + ".py";
		$("#download-link").attr("href", url);
		$("#download-link").attr("download", filename);
	});
	
	//handle validate by URL fields.
	$("#url-checkbox-section input").change(function() {
		if( $("#wtf-validate-by-url-checkbox").is(':checked') ) {
			useUrlValidation = true;
			var validationExpression = $("#wtf-validate-by-url-text").val();
			
			if($("#validate-url-by-regex").is(':checked')) {
				// handle as regex
				var urlPattern = new RegExp(validationExpression);
				if (!urlPattern.test(currentTab.url)) {
					$("#url-checkbox-section").addClass("has-errors");
					return;
				} 				
				urlValidationType = "regex";
				addRegExUser("validate-url");
			} else {
				// handle as substring.
				removeRegExUser("validate-url");
				if ( currentTab.url.indexOf(validationExpression) < 0) {
					$("#url-checkbox-section").addClass("has-errors");
					return;
				}				
				urlValidationType = "substring";
			}
			
			// Means we ran through either validations above.
			$("#url-checkbox-section").removeClass("has-errors");
			urlValidationFilter = validationExpression.replace("\\", "\\\\").replace("'", "\\'");
			
		} else {
			$("#url-checkbox-section").removeClass("has-errors");
			removeRegExUser("validate-url");
			useUrlValidation = false;
		}
		refreshPageObjectPreview();
	});
	
	//handle validate by title fields.
	$("#title-checkbox-section input").change(function() {
		if( $("#wtf-validate-by-title-checkbox").is(':checked') ) {
			useTitleValidation = true;
			var validationExpression = $("#wtf-validate-by-title-text").val();
			
			if($("#validate-title-by-regex").is(':checked')) {
				// handle as regex
				var titlePattern = new RegExp(validationExpression);
				if (!titlePattern.test(currentTab.title)) {
					$("#title-checkbox-section").addClass("has-errors");
					return;
				} 				
				titleValidationType = "regex";
				addRegExUser("validate-title");
			} else {
				// handle as substring.
				removeRegExUser("validate-title");
				if ( currentTab.title.indexOf(validationExpression) < 0) {
					$("#title-checkbox-section").addClass("has-errors");
					return;
				}				
				titleValidationType = "substring";
			}
			
			// Means we ran through either validations above.
			$("#title-checkbox-section").removeClass("has-errors");
			titleValidationFilter = validationExpression.replace("\\", "\\\\").replace("'", "\\'");
			
		} else {
			$("#title-checkbox-section").removeClass("has-errors");
			removeRegExUser("validate-title");
			useUrlValidation = false;
		}
		refreshPageObjectPreview();
	});
	
	//Handle map new element button.
	$("#map-new-element").click(function() {
		chrome.tabs.getSelected(null,function(tab) {
			myTabId = tab.id;
			console.log("Sending map Element message");
			chrome.tabs.sendMessage(currentTab.id, {wtframework: true, action: "mapElement", wtftab:tab.id}, 
					function(response) {

			  });
		});
		chrome.tabs.update(currentTab.id, {active:true}, function(tab) {})
	});
	
	
}); //End of on document ready block.

