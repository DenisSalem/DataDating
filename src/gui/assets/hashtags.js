function appendHashtag(a) {
	ul = $(a.parentNode).children(".displayedData");
	textarea = $(ul.parentNode).children(".data");
	if (a.value != "") {
		ul.append("<li class=\"hashtag\">"+a.value+"</li>");
		$(".hashtag").on('click', function() {
			$(this).remove();
		})
	}
	a.value = "";
}


$(document).ready(function() {
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
