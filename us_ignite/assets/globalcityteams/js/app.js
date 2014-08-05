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
		
		$(window).scroll(function(e){
			parallax();
		});
	});
	
	/* Show content when page loads */
	$(window).load(function (e) {
		$("body").fadeIn(800);
		
	});

})(jQuery);

/* Add parallax effect to intro image */
function parallax(){
	var scrolled_1 = $('body').scrollTop();
	$('.intro-image').css( 'background-position' , '0% -' + (scrolled_1 * 0.35) + 'px' );
}






