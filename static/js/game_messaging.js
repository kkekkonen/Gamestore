$(document).ready(function () {
	function getCookie(name) {
		var cookieValue = null;
		if (document.cookie && document.cookie !== '') {
			var cookies = document.cookie.split(';');
			for (var i = 0; i < cookies.length; i++) {
				var cookie = jQuery.trim(cookies[i]);
				// Does this cookie string begin with the name we want?
				if (cookie.substring(0, name.length + 1) == (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
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
		if(evt.data.messageType === "SAVE" || evt.data.messageType === "SCORE") {
			$.ajax({
				type: "POST",
				url: "http://" + document.getElementById("url").textContent + "/request",
				contentType: 'application/json; charset=utf-8',
				processData: false,
				data: JSON.stringify(evt.data),
				datatype: "json",
			});
		} else if(evt.data.messageType === "LOAD_REQUEST") {
			$.ajax({
				type: "GET",
				url: "http://" + document.getElementById("url").textContent + "/request",
				data: evt.data,
				datatype: "json",
				success: function(response) {
					document.getElementById("iFrameWindow").contentWindow.postMessage(response, "*");
				},
			});
		} else if( evt.data.messageType === "SETTING") {
			var height = Math.min($(window).height()*0.9, evt.data.options.height);
			var width = Math.min($(window).width()*0.9, evt.data.options.width);
			$("#iFrameWindow").width(width).height(height);
		};
	});
});
