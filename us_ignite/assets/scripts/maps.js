var map = {
  /**
     Renders a map from a list of objects
  **/
  render: function(mapLocations) {
    var mapOptions = {
      center: new google.maps.LatLng(41.850033, -87.6500523),
      zoom: 4,
      zoomControl: true,
      zoomControlOptions: {
        position: google.maps.ControlPosition.RIGHT_CENTER
      },
      mapTypeControl: true,
      mapTypeControlOptions: {
        style: google.maps.MapTypeControlStyle.DROPDOWN_MENU
      },
      streetViewControl: false,
      scaleControl: false,
      panControl: false
    };
    var map = new google.maps.Map(document.getElementById("map"), mapOptions);
    for ( i = 0; i < mapLocations.length; i++ ) {
      var m = mapLocations[i];
      var place = new google.maps.LatLng(m.latitude, m.longitude);
      var marker = new google.maps.Marker({
        map: map,
        position: place,
        icon: m.image
      });
    }
  }
};
