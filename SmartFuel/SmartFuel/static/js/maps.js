// This example adds a search box to a map, using the Google Place Autocomplete
// feature. People can enter geographical searches. The search box will return a
// pick list containing a mix of places and predicted search terms.

var map;
var center;
var circle;
var markers = [];
var directionsService = new google.maps.DirectionsService();
var directionsDisplay = new google.maps.DirectionsRenderer();

function initialize() {

  var markers = [];
  map = new google.maps.Map(document.getElementById('map-display'), {
     zoom: 15
  });
    directionsDisplay.setMap(map);
  // Try HTML5 geolocation
        if(navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                center = new google.maps.LatLng(position.coords.latitude,
                    position.coords.longitude);
                getAddress(center);
                showNearestFuelStations(1000);
            }, function() {
                handleNoGeolocation(true);
            });
        } else {
            // Browser doesn't support Geolocation
            handleNoGeolocation(false);
        }
  // Create the search box and link it to the UI element.
  var input = /** @type {HTMLInputElement} */(
      document.getElementById('pac-input'));


  var searchBox = new google.maps.places.SearchBox(
    /** @type {HTMLInputElement} */(input));

  // [START region_getplaces]
  // Listen for the event fired when the user selects an item from the
  // pick list. Retrieve the matching places for that item.
  google.maps.event.addListener(searchBox, 'places_changed', function() {
    var places = searchBox.getPlaces();

    if (places.length == 0) {
      return;
    }
    for (var i = 0, marker; marker = markers[i]; i++) {
      marker.setMap(null);
    }
    // For each place, get the icon, place name, and location.
    markers = [];
    var bounds = new google.maps.LatLngBounds();
    for (var i = 0, place; place = places[i]; i++) {
      var image = {
        url: place.icon,
        size: new google.maps.Size(171, 171),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(17, 34),
        scaledSize: new google.maps.Size(25, 25)
      };

      // Create a marker for each place.
      center = place.geometry.location;
      var marker = new google.maps.Marker({
        map: map,
        icon: image,
        title: place.name,
        position: place.geometry.location
      });
      markers.push(marker);

      bounds.extend(place.geometry.location);
      showNearestFuelStations(1200);
    }

    map.fitBounds(bounds);
  });
  // [END region_getplaces]

  // Bias the SearchBox results towards places that are within the bounds of the
  // current map's viewport.
  google.maps.event.addListener(map, 'bounds_changed', function() {
    var bounds = map.getBounds();
    searchBox.setBounds(bounds);
  });
}
function handleNoGeolocation(errorFlag) {
    if (errorFlag) {
        var content = 'Error: The Geolocation service failed.';
    } else {
        var content = 'Error: Your browser doesn\'t support geolocation.';
    }
    var options = {
        map: map,
        position: new google.maps.LatLng(37.979946, 23.727801),
        content: content
    };

    var infowindow = new google.maps.InfoWindow(options);
    map.setCenter(options.position);
}

function getAddress(latlng) {
    var geocoder = new google.maps.Geocoder();
    return geocoder.geocode({'latLng': latlng}, function(results, status) {
        if(status == google.maps.GeocoderStatus.OK) {
            if (results[1]) {
                map.setCenter(results[0].geometry.location);
                var message = results[0].formatted_address.split(", ")[0]
                    + results[1].formatted_address;
                var marker = new google.maps.Marker({
                  position: latlng,
                  map: map,
                  icon: "http://maps.google.com/mapfiles/ms/icons/blue-dot.png"
                });
                var infowindow = new google.maps.InfoWindow({
                    content: 'Είστε εδώ. ' + message
                });
                infowindow.open(map,marker);
            }
            else {
                alert("No results");
            }
        } else {
            alert("Geocoding unsuccessful: Status " + status);
        }
    });
}

function showNearestFuelStations(radius) {
	$.ajax({
		url: "/nearest",
		dataType: 'json',
		data: {
            fuel: 'unleaded95'
		},
		success: function(data) {
            displayNearestFuelStations(radius, center, data);
		},
		error: function() {
			alert("Κάτι πήγε στραβά παρακαλώ δοκιμάστε ξανά");
		}
	});
}

function markMultipleStations(coordinates, prices, address) {
	var LATITUDE_INDEX = 0;
	var LONGITUDE_INDEX = 1;
    if (markers.length > 0)
        for (var i = 0; i < markers.length; i++) {
            markers[i].setMap(null);
            delete markers[i];
        }
	for(var i = 0; i < coordinates.length; i++) {
        var location = new google.maps.LatLng(parseFloat(coordinates[i][LATITUDE_INDEX]),
            parseFloat(coordinates[i][LONGITUDE_INDEX]));
        var url;
        if (i == 0)
            url = "http://maps.google.com/mapfiles/ms/icons/green-dot.png";
        else
            url = "http://maps.google.com/mapfiles/ms/icons/red-dot.png";
        var marker = new google.maps.Marker({
            map: map,
            position: location,
            icon: url
        });
        markers.push(marker);
        var infowindow = new google.maps.InfoWindow({
            content: prices[i].toFixed(2)
        });
        infowindow.open(map, marker);
    }
}

function displayNearestFuelStations(radius, pos, stations) {
	var coord = [];
    if (circle != undefined && circle != null)
        circle.setMap(null);
	drawCircle(radius, pos);
    circle.setMap(map);
    var prices = [];
    var address = [];
	for(var i = 0; i < stations.length; i++) {
        var lat = stations[i].fields.latitude;
        var lon = stations[i].fields.longitude;
		var location = new google.maps.LatLng(lat, lon);
		if(circle.getBounds().contains(location)) {
            var geo_location = [];
            geo_location.push(lat);
            geo_location.push(lon);
			coord.push(geo_location);
            prices.push(stations[i].fields.unleaded95);
            address.push(stations[i].fields.address);
		}
	}
	markMultipleStations(coord, prices, address);
	map.setZoom(15);
}

function drawCircle(radius, location) {
	var circleInfo = {
		strokeColor: '#FF0000',
		strokeOpacity: 0.6,
		strokeWeight: 2,
		fillColor: '00FFFF',
		fillOpacity: 0.35,
		map: this.map,
		center: location,
		radius: parseInt(radius)

	};
	circle = new google.maps.Circle(circleInfo);
}

function getOptimalStations() {
    $.ajax({
		url: "/optimal",
		dataType: 'json',
		data: {
            consumption: $("#consumption").val(),
            initial: $("#initial").val(),
            fuel: $("#fuel").val(),
            cap: $("#capacity").val()
		},
		success: function(data) {
            alert(data);
		},
		error: function() {
			alert("Κάτι πήγε στραβά παρακαλώ δοκιμάστε ξανά");
		}
	});
}

function calcRoute() {
  var start = "Athens";
  var end = "Thessaloniki";
  var waypts = [{location: 'Lamia', stopover: true},
      {location: "Temph", stopover:true}];


  var request = {
      origin: start,
      destination: end,
      waypoints: waypts,
      optimizeWaypoints: true,
      travelMode: google.maps.TravelMode.DRIVING
  };
  directionsService.route(request, function(response, status) {
    if (status == google.maps.DirectionsStatus.OK) {
      directionsDisplay.setDirections(response);
      var route = response.routes[0];
      var summaryPanel = document.getElementById('directions_panel');
      summaryPanel.innerHTML = '<div class =\"box box-solid collapsed-box\">' +
						'<div class=\"box-header bg-light-blue\">' +
							'<p class = \"text-pos-header\"><span><i>Βέλτιστος ανεφοδιασμός</i></span></p>'+
						'</div>' +
						'<div class=\"box-body\">' +
			'<p><B>Ανεφοδιασμός Α</B>: 12 Ανδρουτσού, Λαμία, ΑΦΟΙ Γεωργίου<br>' +
            '<B>Ποσότητα</B>: 10L, <b>τιμή</B>: 1.242<br><br><br>' +
            '<b>Ανεφοδιασμός Β: </b> 270ο χλμ Εθνικής οδού Λαμία-Θεσαλλονικής, Νίκος Μανιάς<br>' +
            '<B>Ποσότητα</B>: 15L, <b>τιμή</B>: 1.121<br><br><br>' +
            '<b>Συνολικό κόστος</b>: 534.6 ευρώ</p>' +
			'</div>' +
			'</div>';
    }
  });
}

google.maps.event.addDomListener(window, 'load', initialize);