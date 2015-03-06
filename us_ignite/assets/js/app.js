$(document).foundation();

$(function() {
	function split( val ) {
		return val.split( /,\s*/ );
	}
	function extractLast( term ) {
		return split( term ).pop();
	}

	if ($('#id_tags').length) {
		$.getJSON(__SITEURL__ + '/search/tags.json', function(availableTags) {
			$( "#id_tags" )
	        // don't navigate away from the field on tab when selecting an item
	        .bind( "keydown", function( event ) {
	        	if ( event.keyCode === $.ui.keyCode.TAB &&
	        		$( this ).data( "ui-autocomplete" ).menu.active ) {
	        		event.preventDefault();
	        	}
	    	})
	    	.autocomplete({
	        	minLength: 0,
	        	source: function( request, response ) {
	            // delegate back to autocomplete, but extract the last term
	            response( $.ui.autocomplete.filter(
	            	availableTags, extractLast( request.term ) ) );
		        },
		        focus: function() {
		            // prevent value inserted on focus
		            return false;
		        },
		        select: function( event, ui ) {
		        	var terms = split( this.value );
		            // remove the current input
		            terms.pop();
		            // add the selected item
		            terms.push( ui.item.value );
		            // add placeholder to get the comma-and-space at the end
		            terms.push( "" );
		            this.value = terms.join( ", " );
		            return false;
		        }
	    	});
	    });
	}

	/* Hide and trigger ordering form. */
	if ($('#listing-ordering').length) {
		$('#listing-ordering').find('button').hide();
		$('#id_order').change(function(){
			$('#listing-ordering').submit();
		});
	}


	if ($(".summit-container").length > 0) {
		$("body").addClass("app-summit");
		$("body").fadeIn(200);
	}

	if ($(".march-2015-splash").length > 0) {
		$("body").addClass("march-2015");
		$("body").fadeIn(200);
	}

	$('.main-carousel').slick({
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

	/* Open social app summit share buttons in popup windows */
	$('.share-button').on('click', function(e) {
		e.preventDefault();
		window.open($(this).attr('href'), 'sharer', "toolbar=no, width=550, height=550");          
	});

	initTabs();
	renderMobileTabs();
	if ($(".march-2015-splash").length > 0)
	{
		$('.march-2015-splash .partners-grid a ').matchHeight();
	}
	
	centerPartnerImages();
	march2015Parallax();
	setTimeout(function () { 
		responsiveVideos(); 
		$(".responsive-video").fadeTo(400, 1);
	}, 2000);

});

$(window).load(function() {
	
	$(window).trigger('resize');
});

$(window).resize(function() {
	
	march2015Parallax();
	centerPartnerImages();
});

function parallax(){
	var scrolled_1 = $(window).scrollTop();
	var scrolled_2 = scrolled_1 - 1000;
	var scrolled_3 = scrolled_2 - 700;
	var scrolled_4 = scrolled_3 - 700;
	$('.slide--one').css( 'background-position' , 'left -' + (scrolled_1 * 0.35) + 'px' );
	$('.slide--two').css( 'background-position' , 'left -' + (scrolled_2 * 0.35) + 'px' );
	$('.slide--three').css( 'background-position' , 'left -' + (scrolled_3 * 0.35) + 'px' );
	$('.slide--four').css( 'background-position' , 'left -' + (scrolled_4 * 0.35) + 'px' );


}

function march2015Parallax () {
	var scrolled_1 = $(window).scrollTop() - 50;

	var difference;

	if ($("body").width() > 600)
		difference = 2000;
	else
		difference = 2000;
	var headerImageLeft = ( difference - $("body").width()) / 2;
	$('.march-2015 .header-image').css( 'background-position' , "-" + headerImageLeft + 'px -' + ((scrolled_1 * 0.35) + 220) + 'px' );
	$('.march-2015 .header-image').fadeTo(300, 1);
}

function initTabs () {
	$(".tabs-container").each(function () {
		var $tabsContainer = $(this);

		$tabsContainer.find(".tab-bar > a").on("click", function (e) {
			e.preventDefault();

			if ($(this).hasClass("active"))
				return;
			$tabsContainer.find(".tab-bar > a").removeClass("active");
			$(this).addClass("active");
			var section = $(this).data("section");
			$tabsContainer.find(".tab-content > div").removeClass("active");
			$tabsContainer.find("[data-section-name='" + section + "']").addClass("active");

			responsiveVideos();
		});
	});
}

function renderMobileTabs () {
	
	// Create mobile tabs using markup from desktop tabs
	$(".tabs-container").each(function () {
		var $tabsContainer = $(this);
		var mobileTabHtml = '<div class="row"><div class="columns small-12 small-centered "><div class="mobile-tabs-container"><div class="tabs">';

		$tabsContainer.find(".tab-bar > a").each(function () {
			var tabName = $(this).html();
			var section = $(this).data("section");
			var tabContent = $tabsContainer.find("[data-section-name='" + section + "']").html();

			mobileTabHtml += '<div><a href="#" class="handle">' + tabName + ' <div class="close">&#215;</div></a>';
			mobileTabHtml += '<div class="tab-content">' + tabContent + '</div>';
			mobileTabHtml += '</div>';
		});

		mobileTabHtml += '</div></div></div></div>';

		$(mobileTabHtml).insertAfter($tabsContainer);

	});

	
	// Make mobile tabs functional
	$(".mobile-tabs-container").each(function () {
		var $tabsContainer = $(this);

		$tabsContainer.find(".handle").on("click", function (e) {

			$thisHandle = $(this);
			e.preventDefault();

			if ($thisHandle.hasClass("active"))
			{
				$thisHandle.next(".tab-content").slideUp(300, function () {
					$thisHandle.removeClass("active");
				});
			}
			else
			{

				$thisHandle.next(".tab-content").slideDown(300, function () {
					$thisHandle.addClass("active");
					responsiveVideos();
				});
			}
		});
	});


}


function responsiveVideos() {
	 var $allVideos = $(".responsive-video > iframe");
    
	    	
	$allVideos.each(function() {
	
	  $(this)
	    // jQuery .data does not work on object/embed elements
	    .attr('data-aspectRatio', this.height / this.width);
	   // .removeAttr('height')
	    //.removeAttr('width');

	    var newWidth = $(this).closest("figure").width();
	    var $el = $(this);
	    $el
	        .width(newWidth)
	        .height(newWidth * $el.attr('data-aspectRatio'));
	
	});
	
	$(window).resize(function() {
	
	  
	  $allVideos.each(function() {
	  	var newWidth = $(this).closest("figure").width();
	    var $el = $(this);
	    $el
	        .width(newWidth)
	        .height(newWidth * $el.attr('data-aspectRatio'));
	  
	  });
	
	}).resize();

}

function centerPartnerImages () {
	var desktopHeight = $('.march-2015-splash .tabs-container .partners-grid a:first ').height();
	$('.march-2015-splash .tabs-container .partners-grid a').css("line-height", desktopHeight + "px");
	var mobileHeight = $('.march-2015-splash .mobile-tabs-container .partners-grid a:first ').height();
	$('.march-2015-splash .mobile-tabs-container .partners-grid a').css("line-height", mobileHeight + "px");
}

$(window).scroll(function(e){
	march2015Parallax();
});


