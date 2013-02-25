var currentUrl = "N/A";

//on document ready
$(document).ready(function() {


	
	//Format the data URL right before the user clicks on the download link.
	$("#scan-page-button").click(function() {
		chrome.tabs.getSelected(null,function(tab) {
			//pass tab id to new window so new window can reference it.
			chrome.windows.create({'url': 'panel.html?' + tab.id, 'type': 'detached_panel',
				'width':580, 'height':800
				}, function(window) {
					console.log("url got from popup:" + tab.url)
			   });
		});

	});
	
});

