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

//Just a variable I set so i can tell this page from other pages in the chrome debugger.
const wtfContentScript = true;

//flat to turn on/off the click monitoring.
var _wtfMonitorClick = false;
var _wtfTabId = null;

chrome.extension.onMessage.addListener(
		function(request, sender, sendResponse) {
			console.log("I received a message");
			console.log(request);
			
			// Return if message is not passed by WTFramework.
			if (request.wtframework != true)
				return;
			
			
			// Handle the popup sending us the tab URL upon initializing this window.
			if (request.action == "mapElement" && _wtfMonitorClick == false) {
				_wtfMonitorClick = true;
				_wtfTabId = request.wtftab;
				console.log("received map Element message, turning on click monitoring.");
				console.log("WTF Tab id:" + _wtfTabId);
				
				//Display user message to click on element to map.
				alert("\n\nWTFramework\n\nClick on an element on this page to map it.");
			}
			
						
			if (request.action == "checkElement" || request.action == "highlightElement") {
				console.log( request.action + " request received.");
				
				var blinkElement = request.action == "highlightElement";
				
				var checkOk = false;
				var query = request.query;
				try {
					switch(request.by) {
					case 'name':
						console.log("Checking if element exist using name");
						var element = document.evaluate( "//*[@name='" + query + "']" ,document, null, 
								XPathResult.FIRST_ORDERED_NODE_TYPE, null ).singleNodeValue;
						if (element != null) {
							checkOk = true;
							if(blinkElement) {
								blinkIt($(element));
							}
						}
						break;
					case 'id':
						console.log("Checking if element exist using id");
						var element = document.evaluate( "//*[@id='" + query + "']" ,document, null, 
								XPathResult.FIRST_ORDERED_NODE_TYPE, null ).singleNodeValue;
						if (element != null) {
							checkOk = true;
							if(blinkElement) {
								blinkIt($(element));
							}
						}
						break;
					case 'cssSelector':
						console.log("Checking if element exist using cssSelector");
						var element = document.querySelector(query);
						if( element != null) {
							checkOk = true;
							if(blinkElement) {
								blinkIt($(element));
							}
						}
						break;
					case 'xpath':
						console.log("Checking if element exist using xpath");
						var element = document.evaluate( query ,document, null, 
								XPathResult.FIRST_ORDERED_NODE_TYPE, null ).singleNodeValue;
						if (element != null) {
							checkOk = true;
							if(blinkElement) {
								blinkIt($(element));
							}
						}
						break;
					}	
				} catch (e) {
					console.log("did not find element.");
					console.log(e);
				}
				
				
				if (checkOk) {
					sendResponse({result: "OK"});
				} else {
					sendResponse({result: "FAIL"});
				}
			}
			
			
});

//Monitor clicks
//Add a doucment level listener for click events.
document.onclick = function(clickEvent) {
	if (_wtfMonitorClick == true) {
		clickEvent.preventDefault();
		clickEvent.stopPropagation();
		
		_wtfMonitorClick = false;
		
		var clickedElement = $(clickEvent.target);
		var name = clickedElement.attr('name');
		var id = clickedElement.attr('id');
		var xpath = clickedElement.getXPath();
		var cssSelector = clickedElement.getCssPath();
		var text = clickedElement.text();
		var tag = clickedElement.prop("tagName");
		var value = clickedElement.val();
		
		var messagePayload = {
				wtframework:true,
				action: "element-mapped",
				name: name,
				id: id,
				xpath: xpath,
				cssSelector:cssSelector,
				text:text,
				tag:tag,
				value:value
		};

		console.log(messagePayload)
		
		chrome.extension.sendMessage(null, messagePayload, function() {		
		});
	}
	
	
};


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


// Blink a target object.
function blinkIt(target) {
	var x = false;
	console.log("target is" + target);
	
	var oldBorderColor = target.css('border-color');
	var oldBorderStyle = target.css('border-style');
	var oldBorderWidth = target.css('border-width');
	
	console.log("blinking element");
    var blinker = setInterval(function() {
    	if(!x) {
    		console.log("setting border");
        	target.css('border-color', 'red');
        	target.css('border-style', 'solid');
        	target.css('border-width', '5px');	
    	}
    	else {
    		console.log("unsetting border");
        	target.css('border-color', oldBorderColor);
        	target.css('border-style', oldBorderStyle);
        	target.css('border-width', oldBorderWidth);	
    	}
    	x = !x;
    }, 150);
    
    
    setTimeout(function(){
    	window.clearInterval(blinker);
    	console.log("unsetting border");
    	target.css('border-color', oldBorderColor);
    	target.css('border-style', oldBorderStyle);
    	target.css('border-width', oldBorderWidth);
    	},5000);

};
    