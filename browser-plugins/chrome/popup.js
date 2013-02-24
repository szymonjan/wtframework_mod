

//on document ready
$(document).ready(function() {

	//Format the data URL right before the user clicks on the download link.
	$("#scan-page-button").click(function() {
		chrome.windows.create({'url': 'panel.html', 'type': 'detached_panel',
			'width':580, 'height':800
			}, function(window) {
		   });
		//msg this panel the URL.
	});
	
});

