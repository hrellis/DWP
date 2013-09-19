var orange = "#f60";
var white = "#fff";
var red = "#f00";

function changeTextColor(color)
{
	$("body").css("color", color);
	$("a").css("color", color);
	$("a:hover").css("color", color);
	
	$.cookie("textColor",color,{expires: 365, path:'/'});
	console.log("changeTextColor called with color " + color);
}

$(function()
{
	var color = $.cookie("textColor");
	changeTextColor(color);
});