(function ($) {
	$( "#menu-button" ).click(function() {     
		var $elems = $('.jump-to-container, .social-bar');
		if ( $elems.hasClass("active"))
		{
			$elems.removeClass("active");
		}
		else
		{
			$elems.addClass("active");
		}
	});
})(jQuery);