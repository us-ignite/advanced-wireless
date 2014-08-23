'use strict';

$(document).foundation();

(function ($) {
	
	$(function () {
		/* Scroll to content when clicking arrow in intro image */
		$(".down-button").on("click", function (e) {
			var contentTop = $("#content").offset().top;
			$("body").animate({
				scrollTop: contentTop
			}, 400, function () {
				
			});
		});
		
		/* Initialize sponsers/partners carousel */
		$('.carousel').slick({
			 infinite: true,
			speed: 600,
			slidesToShow: 6,
			slidesToScroll: 6,
			autoplay: true,
			responsive: [
				{
					breakpoint: 640,
					settings: {
						slidesToShow: 3,
						slidesToScroll: 3,
						infinite: true,
						dots: false
					}
				}
			]
		});
		
		/* Validate form */
		$("#ss-form").validate({
			onclick: false,
			submitHandler: function(form) {
				form.submit();
			}
			/* End submitHandler */
		});
		
		showHideTopArrow();
		
		$(window).scroll(function(e){
			parallax();
			showHideTopArrow();
		});
		
		$("#top-arrow").on("click", function (e) {
			var faqTopicTop = $("#faq-topics").offset().top;
			$("body").animate({
				scrollTop : faqTopicTop - 20
			});
		});
		
		$("#faq-topics").on("click", function (e) {
			if ($(e.target).is("strong"))
			{
				e.preventDefault();
				var faq = $(e.target).parent().attr("href");
				var newScrollTop = $(faq).offset().top;
				$("body").animate({
					scrollTop : newScrollTop
				});
			}
		});
	});
	
	/* Show content when page loads */
	$(window).load(function (e) {
		$("body").fadeIn(800);
		
	});
	
	
	function showHideTopArrow () {
		var faqTopicTop = $("#faq-topics").offset().top;
		var bodyScrollTop = $("body").scrollTop();
		if (	(bodyScrollTop + 20) >faqTopicTop)
		{
			$("#top-arrow").show();
		}
		else
		{
			$("#top-arrow").hide();
		}
	}

})(jQuery);

/* Add parallax effect to intro image */
function parallax(){
	var scrolled_1 = $(window).scrollTop();
	$('.intro-image').css( 'background-position' , '0% -' + (scrolled_1 * 0.35) + 'px' );
}






