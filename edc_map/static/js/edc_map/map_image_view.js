function mapImageViewReady(jsonData) {

    /*  */
    var djContext = jsonData.replace('\u0027', '"').replace('\u0022', '"');
    
    djContext = JSON.parse(djContext);
    
    var imageFileNames = djContext.image_filenames;
    var zoomLevels = djContext.zoom_levels;
 
    $( '#id-button-back-call' ).click( function () {
        window.location = djContext.back_call_url;
    });
    $( '#id-button-back-subject' ).click( function () {
        window.location = djContext.back_subject_url;
    });

    if ( imageFileNames != null ) {
        // setup images and zoom buttons
        $.each( imageFileNames, function( zoomLevel, imageFilename ) {
            var imageId = 'id-image-map-' + zoomLevel;
            var buttonId = 'id-button-zoom-' + zoomLevel;
            // set the image src for each image 
            makeImgTag( 'div-image-maps-container', imageId, imageFilename );
            // make and append Zoom buttons
            makeDefaultButtonTag( 'div-zoom-buttons-container', buttonId, 'Zoom ' + zoomLevel );
            // set click function for each Zoom button
            $( '#' + 'id-button-zoom-' + zoomLevel ).click( function() {
                $.each( zoomLevels, function( i, val ) {
                    $( '#id-image-map-' + val ).hide();  // hide all images
                    $( '#id-button-zoom-' + val ).removeClass( 'btn-primary' ).addClass( 'btn-default' ); // set all buttons to default
                });  //each            
                // this button has focus
                $( '#id-button-zoom-' + zoomLevel).removeClass( 'btn-default' ).addClass( 'btn-primary' );
                displayImageTagOrAlert(zoomLevel);
            }); // click
        }); // each

        $( '#div-missing-image-alert' ).text( '' ).hide();

        // show landmarks
        $( '#div-landmarks' ).show();

        // click the almost middle zoom level
        key = Math.floor(zoomLevels.length / 2);
        $( '#id-button-zoom-' + zoomLevels[key] ).click();

    } else {
        // or show the missing image alert
        $( '#div-missing-image-alert' ).text( 'No image maps are available for this location' ).show();
    };  // if ( imageFileNames != null )
}

function makeDefaultButtonTag ( divId, buttonId, label ) {
    var cssClass = 'btn btn-sm btn-default';
    var button = '<button id="' + buttonId + '" type="button" class="' + cssClass + '">' + label + '</button>';
    $('#' + divId).append(button);
};

function makeImgTag ( divId, imageId, imageFilename ) {
    var cssClass = 'img-rounded img-responsive';
    var img = '<img id="' + imageId + '" class="' + cssClass + '"/>';
    $('#' + divId).append(img);
    $( '#' + imageId ).attr( 'src', imageFilename ).attr( 'title', imageFilename ).hide();
}

function displayImageTagOrAlert( zoomLevel ) {
    //check if the image exists, otherwise show alert
    $.ajax({
        url: $( '#id-image-map-'+ zoomLevel ).attr( 'src' ),
        type:'HEAD',
        error: function () {
            $( '#id-image-map-' + zoomLevel ).hide();
            $( '#div-missing-image-alert' ).text( 'Image is not available at this zoom level' ).show();
        },
        success: function () {
            $( '#id-image-map-' + zoomLevel ).show();
            $( '#div-missing-image-alert' ).text( '' ).hide();
        },
    });    
}