/*
One line Accessibility Module by Andy Barratt
For more information and instructions on usage, see http://blog.andybarratt.co.uk/?p=426
*/

function changeStyle(ID)
{
	//create cookie to store body style ID in
	var cookieName = 'bodyStyleID=';
	var cookieVal = ID;
	var date = new Date();
	date.setFullYear(date.getFullYear() + 1);	
	var cookieExpires = ';expires=' + date.toGMTString();
	document.cookie = cookieName + cookieVal + cookieExpires+';'+'path=/;';
	//set body's ID to match the chosen colour scheme.
	document.body.id=ID;
}

//-----------------------------------------------------------------------------------------

function changeFontSize(percentage)
{
	//create cookie to store font size in
	var cookieName = 'fontSize=';
	var cookieVal = percentage;
	var date = new Date();
	date.setFullYear(date.getFullYear() + 1);	
	var cookieExpires = ';expires=' + date.toGMTString();
	document.cookie = cookieName + cookieVal + cookieExpires+';'+'path=/;';
	//set body's fontsize to the specified percentage.
	document.body.style.fontSize=percentage;
}
//-----------------------------------------------------------------------------------------

function changeFontFamily(font)
{
	//create cookie to store font size in
	var cookieName = 'fontFamily=';
	var cookieVal = font;
	var date = new Date();
	date.setFullYear(date.getFullYear() + 1);	
	var cookieExpires = ';expires=' + date.toGMTString();
	document.cookie = cookieName + cookieVal + cookieExpires+';'+'path=/;';
	//set body's fontsize to the specified percentage.
	document.body.style.fontFamily=font;
}
//------------------------------------------------------------------------------------------

//load all the cookies that exist into an array
var cookies = document.cookie.split(';');

//create variables to store the cookie values we need in
var bodyStyleID = '';
var percentage = '';

//each cookie that we found
for(i=0;i<cookies.length;i++)
{
	//split the cookie crumbs into the bits we need
	var cookieCrumbs = cookies[i].split('=');
	var cookieName = cookieCrumbs[0].replace(/ /g, '');
	var cookieValue = cookieCrumbs[1];
	
	if(cookieName=='bodyStyleID')
	{
		bodyStyleID = cookieValue;
		document.body.id=bodyStyleID;
	}
	if(cookieName=='fontSize')
	{
		percentage = cookieValue;
		document.body.style.fontSize=percentage;
	}
}

//if no colourScheme cookie found
if(bodyStyleID=='')
{
	document.body.id='default';
}
//if no colour fontSize cookie found
if(percentage=='')
{
	document.body.style.fontSize='100%';
}

document.write('<div id="Accessibility">');

document.write('<a href="javascript:changeStyle(\'default\');" Title="Choose default colour scheme"><img style="vertical-align:middle;" alt="Black On White" src="blackOnWhite.gif" /></a>');

document.write('<a href="javascript:changeStyle(\'whiteOnBlack\');" Title="Choose white on black colour scheme"><img style="vertical-align:middle;" alt="White On Black" src="whiteOnBlack.gif" /></a>');

document.write('<a href="javascript:changeStyle(\'blackOnYellow\');" Title="Choose black on yellow colour scheme"><img style="vertical-align:middle;" alt="Black On Yellow" src="blackOnYellow.gif" /></a>');

document.write('<a href="javascript:changeStyle(\'yellowOnBlack\');" Title="Choose yellow on black colour scheme"><img style="vertical-align:middle;" alt="Yellow On Black" src="yellowOnBlack.gif" /></a>');

document.write('<a href="javascript:changeStyle(\'blackOnPink\');" Title="Choose black on pink colour scheme"><img style="vertical-align:middle;" alt="Black On Pink" src="blackOnPink.gif" /></a>');

document.write('&nbsp;|&nbsp;');

document.write('<a style="text-decoration:none; font-size:16px;" href="javascript:changeFontSize(\'100%\');" Title="Normal Text Size">A</a>');
document.write('<a style="text-decoration:none; font-size:18px;" href="javascript:changeFontSize(\'120%\');" Title="Medium Text Size">A</a>');
document.write('<a style="text-decoration:none; font-size:20px;" href="javascript:changeFontSize(\'140%\');" Title="Large Text Size">A</a>');

document.write('&nbsp;&nbsp;');
document.write('<a style="text-decoration:none; font-family: Dyslexic;" href="javascript:changeFontFamily(\'Dyslexic\');" Title="Open Dyslexic">A</a>');
document.write('<a style="text-decoration:none; font-family: sans-serif;" href="javascript:changeFontFamily(\'sans-serif\');" Title="Sans Serif">A</a>');
document.write('<a style="text-decoration:none; font-family: serif;" href="javascript:changeFontFamily(\'serif\');" Title="Serif">A</a>');
document.write('</div>');













