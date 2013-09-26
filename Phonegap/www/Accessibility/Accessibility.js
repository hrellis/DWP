/*
 * Based on
 * One line Accessibility Module by Andy Barratt
 * For more information and instructions on usage, see http://blog.andybarratt.co.uk/?p=426
 */


// -----------------------------------------------------------------------------------------

function changeFontSize(percentage) {
	// create cookie to store font size in
	localStorage.fontSize = percentage;
	
	// set body's fontsize to the specified percentage.
	setFontSize('body', percentage);
	setFontSize('button', percentage);
	setFontSize('h1', percentage);
	setFontSize('h4', percentage);
	setFontSize('p', percentage);
	setFontSize('span', percentage);
}

function setFontSize(element, percentage) {
	var p = document.getElementsByTagName(element);
	for (i = 0; i < p.length; i++) {
		p[i].style.fontSize = percentage;
	}
}

// ------------------------------------------------------------------------------------------

function changeFont(font) {
	//store the font in local storage
	localStorage.font = font;
	
	//set the body's font to the specified font
	setFont('body', font);
	setFont('button', font);
	setFont('h1', font);
	setFont('h4', font);
	setFont('p', font);
	setFont('span', font);
}

function setFont(element, font) {
	var p = document.getElementsByTagName(element);
	for(i = 0; i <  p.length; i++) {
		p[i].style.fontFamily = font;
	}
}
// ------------------------------------------------------------------------------------------

function changeTheme(id) {
	//store the theme in local storage
	localStorage.theme = id;
	
	//set the body's theme to the specified one 
	setTheme(id);
}

function setTheme(theme) {
	document.body.id = theme;	
}
// ------------------------------------------------------------------------------------------
function restoreStyle(){
	
	if (localStorage.fontSize != undefined){
		changeFontSize(localStorage.fontSize);
	}
	
	if (localStorage.font != undefined){
		changeFont(localStorage.font);
	}
	
	if(localStorage.theme != undefined){
		changeTheme(localStorage.theme);
	}
}

$(document).ready(function(){restoreStyle()});
