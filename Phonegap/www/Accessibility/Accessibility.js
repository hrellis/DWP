/*
 * Based on
 * One line Accessibility Module by Andy Barratt
 * For more information and instructions on usage, see http://blog.andybarratt.co.uk/?p=426
 */
var script = document.createElement('script');
script.src = 'http://code.jquery.com/jquery-1.7.1.min.js';
script.type = 'text/javascript';
document.getElementsByTagName('head')[0].appendChild(script);


function changeStyle(ID) {
	// create cookie to store body style ID in
	var cookieName = 'bodyStyleID=';
	var cookieVal = ID;
	var date = new Date();
	date.setFullYear(date.getFullYear() + 1);
	var cookieExpires = ';expires=' + date.toGMTString();
	document.cookie = cookieName + cookieVal + cookieExpires + ';' + 'path=/;';
	// set body's ID to match the chosen colour scheme.
	document.body.id = ID;
}

// -----------------------------------------------------------------------------------------

function changeFontSize(percentage) {
	// create cookie to store font size in
	localStorage.style = '{"fontSize": "' + percentage + '"}'
	
	// set body's fontsize to the specified percentage.
	setFontSize('button', percentage);
	setFontSize('h4', percentage);
}

function setFontSize(element, percentage) {
	var p = document.getElementsByTagName(element);
	for (i = 0; i < p.length; i++) {
		p[i].style.fontSize = percentage
	}
}

// ------------------------------------------------------------------------------------------

function restoreStyle(){
	var style = localStorage.style;
	
	if (style != undefined){
		style = JSON.parse(style);
		changeFontSize(style.fontSize);
	}
}

$(document)
.ready(function(){restoreStyle()});
