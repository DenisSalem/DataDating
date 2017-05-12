function refreshHashtags(ul) {
	textarea = ul.parent().children(".data");
	var outputData = "";
	ul.children("li").each(function() {
		outputData+= $(this).text()+'|';
	});
	$(textarea).text(outputData);
}

function appendHashtag(a) {
	ul = $(a.parentNode).children(".displayedData");
	if (a.value != "") {
		ul.append("<li class=\"hashtag\">"+a.value+"</li>");
		$(".hashtag").on('click', function() {
			$(this).remove();
			refreshHashtags(ul);
		})
		refreshHashtags(ul);
	}
	a.value = "";
}

$(document).ready(function() {

	$(".hashtags").each( function() {
		$(this).append("<textarea class=\"data\" name=\""+$(this).attr("ht-name")+"\">"+$(this).attr("ht-default-value")+"</textarea>");
		ul = $("<ul class=\"displayedData\"></ul>");
		hashtags = $(this).attr("ht-default-value").split("|");
		for (var i=0; i < hashtags.length; i++) {
		  	if (hashtags[i] != "") {
				ul.append("<li class=\"hashtag\">"+hashtags[i]+"</li>");
			}
		}
		$(this).append(ul);
		$(this).append("<input type=\"text\" value=\"\" class=\"inputData\" />");
	});

	$(".hashtags .inputData").keypress(function( event ) {
		if ( event.which == 13 ) {
			event.preventDefault();
			appendHashtag(this);
		}
		else if (event.which == 8) {
		  	if (this.value == "") {
				ul = $(this.parentNode).children(".displayedData");
				ul.children("li:last-child").remove();
				refreshHashtags(ul);
			}
		}
	});

	$(".hashtags").click(function() {
	  	$(this).children("input").focus();
	});


	$(".hashtags input").bind('blur', function() {
		appendHashtag(this);
	});
});
