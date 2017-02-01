(function ($) {
	$(function () {
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

		$("div.video").fitVids();

		$("#jump-to-pitch").on("change", function (e) {
			var val = $(this).val();
			$("html, body").animate({ scrollTop: $('#' + val).offset().top }, 1000);

		});
	});

})(jQuery);