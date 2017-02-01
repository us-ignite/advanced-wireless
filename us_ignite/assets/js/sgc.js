(function ($) {
	$(function () {
		$(document).foundation();

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
			$("html, body").animate({ scrollTop: $('#' + val).offset().top }, 700);

		});

		$("#back-to-top span").on("click", function (e) {
			
			$("html, body").animate({ scrollTop: "0"}, 700);

		});
	});

})(jQuery);