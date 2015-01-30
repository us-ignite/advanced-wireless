'use strict';

(function ($) {
	
	$(function () {

		$(".no-link").click(function (e) {

			e.preventDefault();
		});

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
			showHideTopArrow();
		});
		
		$("#top-arrow").on("click", function (e) {
			var pageTop = $("body").offset().top;
			$("body").animate({
				scrollTop : pageTop
			});
		});
		
		
		faqScroll();
		uploadForm();
		
		if (getUrlVars()['upload'])
		{
			uploadSuccess();
		}

		//$('.homepage-grid .homepage-grid__heading').matchHeight();
		$('.homepage-grid .homepage-grid__desc ').matchHeight();
	});
	/* end jQuery ready */
	
	/* Show content when page loads */
	$(window).load(function (e) {
		$("body").fadeIn(800);
		
	});
	
	function faqScroll () {
		$("#faq-topics a").each(function (i, el) {
			$(this).attr("href", "#" + i);
		});

		$(".faq-list li").each(function (i, el) {
			$(this).attr("id", i);
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
	}

	/* Show/hide back to top arrow on scroll */
	function showHideTopArrow () {
		if ($("#faq-topics").length < 1)
		{
			return;
		}
		
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
	
	/* Show the upload success modal */
	function uploadSuccess () {
		$(".modal-overlay").fadeIn(500);
		setTimeout(function () {
			$(".modal-overlay").fadeOut(500);
		}, 3000);
	}
	
	/* Handles the Wufoo upload form */
	function uploadForm() {
		if ($("#saveForm").length < 1)
			return;
		
		/* Trigger the file choose dialog */	
		$("#choose-file").on("click", function (e) {
			e.preventDefault();
			$("#Field1").trigger("click");
		});
		
		/* Display the filename in the faux file field when a file is chosen */
		$("#Field1").on("change", function (e) {
			var filename = $(this).val();
			
			var lastIndex = filename.lastIndexOf("\\");
			if (lastIndex >= 0) {
				filename = filename.substring(lastIndex + 1);
			}
			$("#filename").text(filename);	
		});
		
		/* When clicking the submit button, validate the file type */
		$("#saveForm").on("click", function(e) {
			e.preventDefault();
			$("#file-error").slideUp(200);
			
			var $fileInput = $("#Field1");
			
			var validExts = [".doc", ".docx", ".txt", ".pdf", ".rtf"];
			var filename = $fileInput.val();
			var fileExt = filename.substring(filename.lastIndexOf('.'));
			
			/* If valid extension is not found in filename, show error message */
			if (validExts.indexOf(fileExt) < 0) 
			{
				$("#file-error").slideDown(200);
				return false;
    			}
			else
			{
				$("#form1").submit();
			}
		});
	}
	
	/* Get URL query variables */
	function getUrlVars() {
		var vars = {};
		var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
			vars[key] = value;
		});
		return vars;
	}
	
	$("#nist-table tr").each(function () {
		$(this).find("td:eq(5)").remove();
		$(this).find("th:eq(5)").remove();	
	});

	$("#nist-table tbody > tr").each(function (i, el) {
		$(this).find("td:first").html(i + 1);
		
	});
	
	/* Initialize datatables */
	$("#nist-table").DataTable({
		responsive: true,
		"pageLength": 25
	});
	


})(jQuery);






