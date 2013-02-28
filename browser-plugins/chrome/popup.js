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

