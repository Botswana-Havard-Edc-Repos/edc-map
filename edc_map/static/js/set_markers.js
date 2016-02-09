/**
 * @name setMarkers
 *  An setLandMarks set a array of landmarks ploting points on a map.
 * @param {map} google map instance 
 * @param {landmarks} array of landmark points as coordinates, [location name, lat, lon, elevation].
 */

function setMarkers(map, locations) {
	// Add markers to the map
  
	// Shapes define the clickable region of the icon.
	// The type defines an HTML &lt;area&gt; element 'poly' which
	// traces out a polygon as a series of X,Y points. The final
	// coordinate closes the poly by connecting to the first
	// coordinate.
	var shape = {
		coord: [1, 1, 1, 20, 18, 20, 18, 1],
		type: 'poly'
	};
	for (var i = 0; i < locations.length; i++) {
		
		var location_latLon = locations[i];
		
		// Marker sizes are expressed as a Size of X,Y
		// where the origin of the image (0,0) is located
		// in the top left of the image.
		
		// Origins, anchor positions and coordinates of the marker
		// increase in the X direction to the right and in
		// the Y direction down.
		
		var image = new google.maps.MarkerImage(location_latLon[3], // This marker is 20 pixels wide by 32 pixels tall.
			new google.maps.Size(20, 32), // The origin for this image is 0,0.
			new google.maps.Point(0, 0), // The anchor for this image is the base of the flagpole at 0,32.
			new google.maps.Point(0, 32));
		
		var shadow = new google.maps.MarkerImage(location_latLon[3], // The shadow image is larger in the horizontal dimension
		// while the position and offset are the same as for the main image.
		new google.maps.Size(37, 32), new google.maps.Point(0, 0), new google.maps.Point(0, 32));
				
		var myLatLng = new google.maps.LatLng(location_latLon[1], location_latLon[2]);
		var marker = new google.maps.Marker({
			position: myLatLng,
			map: map,
			shadow: shadow,
			icon: image,
			shape: shape,
			title: location_latLon[0],
			zIndex: location_latLon[4]
		});
		
		//call blindInfoWindow function to create an information window for each marker
		var label = "identifier: " + location_latLon[0] + location_latLon[5]
		bindInfoWindow(marker, map, infoWindow, label);
	}
}