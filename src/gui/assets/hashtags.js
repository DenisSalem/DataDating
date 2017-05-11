function appendHashtag(a) {
	ul = $(a.parentNode).children(".displayedData");
	textarea = $(ul.parentNode).children(".data");
	if (a.value != "") {
		ul.append("<li class=\"hashtag\">"+a.value+"</li>");
		$(".hashtag").on('click', function() {
			$(this).remove();
		})
		var outputData = "";
		ul.children("li").each(function() {
			outputData+= $(this).text()+'|';
		});
		
		alert($(textarea).attr("class"));
	}
	a.value = "";
}


$(document).ready(function() {

	$(".hashtags").each( function() {
		$(this).append("<textarea class=\"data\" name=\""+$(this).attr("ht-name")+"\">"+$(this).attr("ht-default-value")+"</textarea>");
		ul = $("<ul class=\"displayedData\"></ul>");
		hashtags = $(this).attr("ht-default-value").split("|");
		for (var i=0; i < hashtags.length; i++) {
			ul.append("<li class=\"hashtag\">"+hashtags[i]+"</li>");
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
				$(this.parentNode).children(".displayedData").children("li:last-child").remove();
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
