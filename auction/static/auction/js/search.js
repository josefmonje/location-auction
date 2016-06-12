google.maps.event.addDomListener(window, 'load', function () {
    var swBound = new google.maps.LatLng(49.00, -8.00);
    var neBound = new google.maps.LatLng(61.00, -1.00);
    var uk = new google.maps.LatLngBounds(swBound, neBound);
	var options = {
		types: ['geocode'],
		bounds: uk
	}
	var places = new google.maps.places.Autocomplete(document.getElementById('location'), options);
	google.maps.event.addListener(places, 'place_changed', function () {
		var place = places.getPlace();
		var address = place.formatted_address;
		var latitude = place.geometry.location.k;
		var longitude = place.geometry.location.D;
        var qs = '?';
        qs = qs + 'latitude=' + latitude + '&longitude=' + longitude;
        qs = qs + '&radius=' + 3;
		document.getElementById('search').href = '../search/#/' + qs;
	});
});
