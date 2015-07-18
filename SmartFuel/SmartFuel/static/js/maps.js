var map;
function initialize() {
    var mapOptions = {
        zoom: 15
    };
    map = new google.maps.Map(document.getElementById('map-display'),
        mapOptions);

        // Try HTML5 geolocation
        if(navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                var pos = new google.maps.LatLng(position.coords.latitude,
                    position.coords.longitude);
                getAddress(pos);
                map.setCenter(pos);
            }, function() {
                handleNoGeolocation(true);
            });
        } else {
            // Browser doesn't support Geolocation
            handleNoGeolocation(false);
        }
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
                var infowindow = new google.maps.InfoWindow({
                    map: map,
                    position: latlng,
                    content: 'Είστε εδώ. ' + message
                });
            }
            else {
                alert("No results");
            }
        } else {
            alert("Geocoding unsuccessful: Status " + status);
        }
    });
}

            google.maps.event.addDomListener(window, 'load', initialize);
