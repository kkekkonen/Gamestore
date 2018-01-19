$(document).ready(function () {
	function getCookie(name) {
		var cookieValue = null;
		if (document.cookie && document.cookie != '') {
			var cookies = document.cookie.split(';');
			for (var i = 0; i < cookies.length; i++) {
				var cookie = jQuery.trim(cookies[i]);
				// Does this cookie string begin with the name we want?
				if (cookie.substring(0, name.length + 1) == (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				};
			};
		};
		return cookieValue;
	};
	var csrftoken = getCookie('csrftoken');
	function csrfSafeMethod(method) {
		// these HTTP methods do not require CSRF protection
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	};
	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			};
		}
	});
	"use strict";
	window.addEventListener("message", function(evt) {
		if(evt.data.messageType === "SCORE" || evt.data.messageType === "SAVE") {
			$.ajax({
				type: "POST",
				url: window.location.href + "/request",
				data: evt.data,
				datatype: "json",
			});
		} else if(evt.data.messageType === "LOAD_REQUEST") {
			$.ajax({
				type: "GET",
				url: window.location.href + "/request",
				data: evt.data,
				datatype: "json",
				success: function(response) {
					document.getElementById("iFrameWindow").contentWindow.postMessage(response, "*");
				},
			});
		} else if( evt.data.messageType === "SETTING") {
			$("#iFrameWindow").width(evt.data.options.width).height(evt.data.options.height);
		};
	});
});
