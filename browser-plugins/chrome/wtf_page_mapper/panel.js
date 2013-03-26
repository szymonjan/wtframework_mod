//This file is part of WTFramework. 
//
//    WTFramework is free software: you can redistribute it and/or modify
//    it under the terms of the GNU General Public License as published by
//    the Free Software Foundation, either version 3 of the License, or
//    (at your option) any later version.
//
//    WTFramework is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU General Public License for more details.
//
//    You should have received a copy of the GNU General Public License
//    along with WTFramework.  If not, see <http://www.gnu.org/licenses/>.



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

//counter that increments so we identify each mapped element uniquely.
var mappedElementCounter = 0;

//parse out currentUrl of host page.
var getParams = location.search.substr(location.search.indexOf("?")+1);


currentTab = chrome.tabs.get(parseInt(getParams), function(tab) {
	
	currentTab = tab;
	currentUrl = urlValidationFilter = tab.url;
	currentTitle = titleValidationFilter = tab.title;
	
	console.log("Url:" + currentUrl);
	
	$("#wtf-validate-by-url-text").val(tab.url);
	$("#wtf-validate-by-title-text").val(tab.title);
	
	//Initial PageObj view.
	refreshPageObjectPreview();
});

function getQueryMethod(mappedElementControl) {

	console.log("element validation type:" + mappedElementControl.find("select").val());

	switch(mappedElementControl.find("select").val()) {
	case "name":
		return "name";
	case "id":
		return "id"
	case "css":
		console.log("doing element css verification");
		return "cssSelector";
		break;
	case "xpath":
		console.log("doing element xpath verification");
		return "xpath";
	}
}

function processElementName(elementName) {
	return (elementName).toLowerCase().replace(/[^a-z]+/g,"_");
}


//Add an mapped element to our mapped elements section.
function appendNewMappedElement(elementData) {
	//append mapped element to mapped-element-container
	var mappedElementControl = $(
		"<div class=\"element-holder\">"+
		"<input type=\"hidden\" class=\"props\" value=\"" + encodeURI(JSON.stringify(elementData))+"\"/>" + 
		"<table>"+
		"<thead><tr>"+
		"<th>ObjectName</th><th>Find Element By</th><th>Find by criteria</th><th></th></tr>" +
		"</tr></thead>"+
		"<tr><td><input name=\"object-name\" type=\"text\"/></td>"+
		"<td>"+
		"<select name=\"find-by\">"+
		"<option value=\"name\">Name</option>"+					
		"<option value=\"id\">Id</option>"+
		"<option value=\"css\">CSS Selector</option>"+
		"<option value=\"xpath\">XPath</option>"+
		"</select>"+
		"</td>"+
		"<td><input name=\"selection-string\" type=\"text\"/></td>"+
		"<td><button class=\"delete-mapped-element\">Remove</button></td>"+
		"<td><button class=\"check-element-button\">Check</button></td>"+ 
		"</tr></table>"+
		"<div class=\"error-message\">Current selector does not map to an element on this page.</div>"+
		"</div>");
	
	//Set initial values for mapped element fields if provided.
	if(elementData != null) {
		if (typeof(elementData.name) != "undefined" ) {
			console.log("Switching to name verification");
			mappedElementControl.find("select[name='find-by']").val("name");
			var processedName = processElementName(elementData.name);
			mappedElementControl.find("input[name='object-name']").val(processedName);
			mappedElementControl.find("input[name='selection-string']").val(elementData.name);
		} else if (typeof(elementData.id) != "undefined" ) {
			console.log("Switching to id verification");
			mappedElementControl.find("select[name='find-by']").val("id");
			var processedName = processElementName(elementData.id);
			mappedElementControl.find("input[name='object-name']").val(processedName);
			mappedElementControl.find("input[name='selection-string']").val(elementData.id);
		} else if (typeof(elementData.cssSelector) != "undefined" ) {
			console.log("Switching to css verification");
			mappedElementControl.find("select[name='find-by']").val("css");
			var processedName;
			if (elementData.text != 'undefined') {
				processedName = processElementName(elementData.text+ "_" + elementData.tag);	
			} else {
				processedName = processElementName(elementData.value+ "_" + elementData.tag);
			}
			mappedElementControl.find("input[name='object-name']").val(processedName);
			mappedElementControl.find("input[name='selection-string']").val(elementData.cssSelector);
		} else if (typeof(elementData.xpath) != "undefined" ) {
			console.log("Switching to xpath verification");
			mappedElementControl.find("select[name='find-by']").val("xpath");
			var processedName;
			if (elementData.text != 'undefined') {
				processedName = processElementName(elementData.text+ "_" + elementData.tag);	
			} else {
				processedName = processElementName(elementData.value+ "_" + elementData.tag);
			}
			mappedElementControl.find("input[name='object-name']").val(processedName);
			mappedElementControl.find("input[name='selection-string']").val(elementData.xpath);
		}
	}


	//add mapped element to our mapped-element-container area.
	$("#mapped-element-container").append(mappedElementControl);

	
	mappedElementControl.find("button.delete-mapped-element").click(function(event){
		event.preventDefault();
		event.stopPropagation();
		//Remove the parent element holder div.
		mappedElementControl.remove();
		console.log("remove button clicked.");
		
		refreshPageObjectPreview();
	});
	
	mappedElementControl.find("button.check-element-button").click(function(event){
		event.preventDefault();
		event.stopPropagation();
		
		rawProps = mappedElementControl.find("input.props").val();
		props = JSON.parse(decodeURI(rawProps));
		console.log(props);
		
		var filterTextInput = mappedElementControl.find("input[name='selection-string']").val();
		
		//Perform validation of find by criteria.
		var queryBy = getQueryMethod(mappedElementControl);
		
		var params = {wtframework: true, action: "highlightElement", by:queryBy, query:filterTextInput};
		console.log("Sending message to content script.");
		console.log(params);
		
		chrome.tabs.sendMessage(currentTab.id, 
				params, 
				function(response) {}
		);//end chrome tab call.
		
		console.log("checking element");
	});
	
	//Add a listner to handle change event on the mapped element.
	mappedElementControl.find("input[name='selection-string']").change(function(event){
		event.preventDefault();
		event.stopPropagation();
		console.log("Input has changed.");
		rawProps = mappedElementControl.find("input.props").val();
		props = JSON.parse(decodeURI(rawProps));
		console.log(props);
		
		var filterTextInput = mappedElementControl.find("input[name='selection-string']").val();
		
		//Perform validation of find by criteria.
		var queryBy = getQueryMethod(mappedElementControl);
		var params = {wtframework: true, action: "checkElement", by:queryBy, query:filterTextInput};
		console.log("Sending message to content script.");
		console.log(params);
		
		chrome.tabs.sendMessage(currentTab.id, 
				params, 
				function(response) {
					console.log(response.result);
					
					if (response.result == "OK") {
						//validation in switch statements have passed.
						mappedElementControl.removeClass("has-errors");
						refreshPageObjectPreview();	
					} else {
						//validation in switch statements have passed.
						mappedElementControl.addClass("has-errors");
						mappedElementControl.find(".error-message").text(
								"Current element selector does not match an element on this page."
						);
					}
				}
		);//end chrome tab call.
	});//End of selection string change listener.
	
	mappedElementControl.find("select").change(function(event){
		event.preventDefault();
		event.stopPropagation();
		console.log("findby select has changed.");
		rawProps = mappedElementControl.find("input.props").val();
		props = JSON.parse(decodeURI(rawProps));
		console.log(props);
		
		switch(mappedElementControl.find("select").val()) {
		case "name":
			console.log("Switching to name verification");
			mappedElementControl.find("input[name='selection-string']").val(props.name);
			break;
		case "id":
			console.log("Switching to id verification");
			mappedElementControl.find("input[name='selection-string']").val(props.id);
			break;
		case "css":
			console.log("Switching to css verification");
			mappedElementControl.find("input[name='selection-string']").val(props.cssSelector);
			break;
		case "xpath":
			console.log("Switching to xpath verification");
			mappedElementControl.find("input[name='selection-string']").val(props.xpath);
			break;
		default:
			console.log("Invalid selection.")
		}
		
		refreshPageObjectPreview();
	});
	
	mappedElementControl.find("input[name='object-name']").change(function(event){

		var name_pattern = /^[a-zA-Z_][0-9a-zA-Z_]*$/;
		if(!name_pattern.test(mappedElementControl.find("input[name='object-name']").val())) {
			mappedElementControl.find(".error-message").text(
					"Invalid Python variable name."
			);
			mappedElementControl.addClass("has-errors");
		} else {
			mappedElementControl.removeClass("has-errors");
			refreshPageObjectPreview();	
		}					
	});
	
	//Refocus on this window.
	chrome.tabs.update(myTabId, {active:true}, function(tab) {});
	refreshPageObjectPreview();
}	//End of add mapped element.


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
				
				appendNewMappedElement(request);

			} //End of listener function.
			
});//end of add listener code.

function generateObjectMapEntry(mappingEntryDiv) {
	var divElement = $(mappingEntryDiv);
	var name = divElement.find("input[name='object-name']").val();
	var queryStr = divElement.find("input[name='selection-string']").val();
	
	var findBy = null;
	switch(divElement.find("select[name='find-by']").val()) {
	case "name":
		findBy = "find_element_by_name";
		break;
	case "id":
		findBy = "find_element_by_id";
		break;
	case "css":
		findBy = "find_element_by_css_selector";
		break;
	case "xpath":
		findBy = "find_element_by_xpath";
		break;
	}
	var objPyCode =
		"    " + name + " = lambda self:self.webdriver." + findBy + "(\"" + queryStr + "\")";
	console.log("obj pycode:\n" + objPyCode);
	return  objPyCode;
 
}

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
"from wtframework.wtf.web.page import PageObject, InvalidPageError"
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
	// Generate entries for mappings for each mapping element div inside mapped-element-container
	var mappingDivs = $("#mapped-element-container").find("div.element-holder");
	for(var i=0; i<mappingDivs.length; i++) {
		code.push(generateObjectMapEntry(mappingDivs[i]));
	}
	
	code.push(
"    ### End Page Elements Section ###",
"",
""
	);	
	
	
	
	//Validation code
	code.push(
"    def _validate_page(self, webdriver):",
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
	
	//Insert an example page object function.
	code.push("\n\n");
	code.push(
"#    # Insert your page object methods here. Example:",
"#    def do_login(username, password):",
"#        #You can refer to your mapped elements by calling them like functions.",
"#        self.username_input().send_keys(username)",
"#        self.password_input().send_keys(password)",
"#        self.submit_button().click()",
"\n"
	);
	
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
	
	//Handle manually map element button.
	$("#manually-map-new-element").click(function() {
		appendNewMappedElement(null);
	});
	

	
	
}); //End of on document ready block.

