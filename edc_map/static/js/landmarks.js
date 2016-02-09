/**
 * @name setLandMarks
 *  An setLandMarks set a array of landmarks ploting points on a map.
 * @param {map} google map instance 
 * @param {landmarks} array of landmark points as coordinates, [location name, lat, lon, elevation].
 */

/*jslint browser:true */
/*global google */


function setLandMarks(map, locations) {
	 // Add markers to the map
	 
	 // Marker sizes are expressed as a Size of X,Y
	 // where the origin of the image (0,0) is located
	 // in the top left of the image.
	 
	 // Origins, anchor positions and coordinates of the marker
	 // increase in the X direction to the right and in
	 // the Y direction down.
	 var image = new google.maps.MarkerImage('http://maps.google.com/mapfiles/arrow.png', // This marker is 20 pixels wide by 32 pixels tall.
	 new google.maps.Size(35, 40), // The origin for this image is 0,0.
	 new google.maps.Point(0, 0), // The anchor for this image is the base of the flagpole at 0,32.
	 new google.maps.Point(0, 32));
	 var shadow = new google.maps.MarkerImage('http://goo.gl/g1PTn', // The shadow image is larger in the horizontal dimension
	 // while the position and offset are the same as for the main image.
	 new google.maps.Size(37, 32), new google.maps.Point(0, 0), new google.maps.Point(0, 32));
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
	   var beach = locations[i];
	   var myLatLng = new google.maps.LatLng(beach[1], beach[2]);
	   var marker = new google.maps.Marker({
	     position: myLatLng,
	     map: map,
	     shadow: shadow,
	     icon: image,
	     shape: shape,
	     title: beach[0],
	     zIndex: beach[3]
	   });
	   
	   var boxText = document.createElement("div");
	       boxText.style.cssText = "border: 0px solid black; margin-top: 8px; background: white; padding: 3px;";
	       boxText.innerHTML = beach[0];
	               
	   var myOptions = {
	            content: boxText
	           ,disableAutoPan: false
	           ,maxWidth: 0
	           ,pixelOffset: new google.maps.Size(-140, 0)
	           ,zIndex: null
	           ,boxStyle: { 
	             background: "url('tipbox.gif') no-repeat"
	             ,opacity: 0.75
	             ,width: "280px"
	            }
	           ,closeBoxMargin: "10px 2px 2px 2px"
	           ,closeBoxURL: "http://www.google.com/intl/en_us/mapfiles/close.gif"
	           ,infoBoxClearance: new google.maps.Size(1, 1)
	           ,isHidden: false
	           ,pane: "floatPane"
	           ,enableEventPropagation: false
	   };
	   var ib = new InfoBox(myOptions);
	   ib.open(map, marker);
	}
}
