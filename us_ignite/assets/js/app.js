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
 });

$(window).load(function() {
  $(window).trigger('resize');
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


function attachScrollListener () {
	$(window).scroll(function(e){
		parallax();
	});
}

attachScrollListener();
