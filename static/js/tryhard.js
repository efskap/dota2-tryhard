$("document").ready(function () {

	$.ajaxSetup({
		cache : false
	});
	var ajax_load = "<img class='spinner center' src='css/img/bx_loader.gif' alt='loading...' />";

	//  load() functions
	var loadUrl = "compute";

	$("#submit").click(function () {
		
		$("#results").html(ajax_load).load(loadUrl,$('#picks').serializeArray());
		return false;

	});
$("#toggle_faq").click(function () {

		$("#faq").slideToggle(200);

	});
});

