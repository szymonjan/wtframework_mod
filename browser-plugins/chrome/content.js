//Just a variable I set so i can tell this page from other pages in the chrome debugger.
const wtfContentScript = true;

//flat to turn on/off the click monitoring.
var _wtfMonitorClick = false;
var _wtfTabId = null;

chrome.extension.onMessage.addListener(
		function(request, sender, sendResponse) {
			console.log("I received a message");
			
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
		
		var messagePayload = {
				wtframework:true,
				action: "element-mapped",
				name: name,
				id: id,
				xpath: xpath,
				cssSelector:cssSelector
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