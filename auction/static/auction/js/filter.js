google.load( 'visualization', '1', {
	'packages': [ 'corechart', 'table', 'geomap' ]
} );

function initialize( ) {
	google.maps.visualRefresh = true;
	var isMobile = ( navigator.userAgent.toLowerCase( ).indexOf( 'android' ) > -1 ) || (                               navigator.userAgent.match( /(iPod|iPhone|iPad|BlackBerry|Windows Phone|iemobile)/ ) );
	if( isMobile ) {
		var viewport = document.querySelector( "meta[name=viewport]" );
		viewport.setAttribute( 'content', 'initial-scale=1.0, user-scalable=no' );
	}
	var mapDiv = document.getElementById( 'googft-mapCanvas' );
	mapDiv.style.width = isMobile ? '100%' : '100%';
	mapDiv.style.height = isMobile ? '100%' : '100%';
	var map = new google.maps.Map( mapDiv, {
		center: new google.maps.LatLng( 51.52877283676188, -0.1789893807494991 ),
		zoom: 10,
		mapTypeId: google.maps.MapTypeId.ROADMAP
	} );
	map.controls[ google.maps.ControlPosition.RIGHT_BOTTOM ].push( document.getElementById( 'googft-legend-open' ) );
	map.controls[ google.maps.ControlPosition.RIGHT_BOTTOM ].push( document.getElementById( 'googft-legend' ) );

	map.data.setStyle( function( feature ) {
		return {
			icon: '/static/auction/images/map_dot.png',
		};
	} );

	map.data.loadGeoJson( '/mapapi/auction-data/' );

	var infoWindow;
	map.data.addListener( 'click', function( event ) {
		//show an infowindow on click
		if( infoWindow != null ) {
			infoWindow.setMap( null );
		}
		var viewing_time=event.feature.getProperty( "viewing_time" );
		if(viewing_time==null){
			viewing_time='';
		}
		infoWindow = new google.maps.InfoWindow( {

			content: '<div style="width: 654px; height: 215px;">' + 
			'<div class="" style="font-family: Roboto,Arial,sans-serif; font-size: small">' + 
			'<div>' + '<div class="googft-info-window" style="overflow-y:auto">' + 
			'<div style="float:left;border:12px">' + '<a href="../../detail/' 
			+ event.feature.getProperty( "pk" ) + '"><img height="150" style="vertical-align:top" src="' 
			+ event.feature.getProperty( "image_src" ) + '"></a>' + '<br>' + '</div>' + '<div style="padding-left:20px;text-align: center;line-height: 200%;">' + 
			'<p style="margin-left:200px;margin-right:100px">' + event.feature.getProperty( "guide_price" ) + 
			'<br>' + event.feature.getProperty( "address" ) + '<br>' + event.feature.getProperty( "description" )
			+ '<br>' + event.feature.getProperty( "auctioneer" ) + ', ' + event.feature.getProperty( "auction_date" ) + ', Lot Number:'
 			+ event.feature.getProperty( "lot" ) + '<br>Viewing Times:<br>'+viewing_time+'<br></p></div></div></div></div></div>',
			map: map,
		} );
		var anchor = new google.maps.MVCObject( );
		anchor.set( "position", event.latLng );
		infoWindow.open( map, anchor );
	} );

	google.maps.event.addDomListener( document.getElementById( 'submit' ), 'click', function( ) {
		var pricemin = document.getElementById( 'minPrice' );
		var strpricemin = pricemin.options[ pricemin.selectedIndex ].value;
		var pricemax = document.getElementById( 'maxPrice' );
		var strpricemax = pricemax.options[ pricemax.selectedIndex ].value;

		var varAuctioneer = document.getElementById( 'SelectAuctioneer' );
		var Auctioneer = varAuctioneer.options[ varAuctioneer.selectedIndex ].value;

		var varVendor = document.getElementById( 'Selectvendor' );
		var vendor = varVendor.options[ varVendor.selectedIndex ].value;
		var varwhere = "Price >= " + strpricemin + " AND Price <= " + strpricemax;

		if( Auctioneer != 0 && vendor != 0 ) {
			map.data.forEach( function( feature ) {
				map.data.remove( feature );
			} );

			map.data.loadGeoJson( '/mapapi/auction-data/?minprice=' + strpricemin + "&maxprice=" + strpricemax + "&auctioneer=" + encodeURIComponent(Auctioneer) + "&vendor=" + encodeURIComponent(vendor) );
		} else if( Auctioneer != 0 && vendor == 0 ) {
			map.data.forEach( function( feature ) {
				map.data.remove( feature );
			} );
			map.data.loadGeoJson( '/mapapi/auction-data/?minprice=' + strpricemin + "&maxprice=" + strpricemax + "&auctioneer=" + encodeURIComponent(Auctioneer) );
		} else if( Auctioneer == 0 && vendor != 0 ) {
			map.data.forEach( function( feature ) {
				map.data.remove( feature );
			} );
			map.data.loadGeoJson( '/mapapi/auction-data/?minprice=' + strpricemin + "&maxprice=" + strpricemax + "&vendor=" + encodeURIComponent(vendor) );
		} else if( Auctioneer == 0 && vendor == 0 ) {
			map.data.forEach( function( feature ) {
				map.data.remove( feature );
			} );
			map.data.loadGeoJson( '/mapapi/auction-data/?minprice=' + strpricemin + "&maxprice=" + strpricemax );
		}
	} );

	if( isMobile ) {
		var legend = document.getElementById( 'googft-legend' );
		var legendOpenButton = document.getElementById( 'googft-legend-open' );
		var legendCloseButton = document.getElementById( 'googft-legend-close' );
		legend.style.display = 'none';
		legendOpenButton.style.display = 'block';
		legendCloseButton.style.display = 'block';
		legendOpenButton.onclick = function( ) {
			legend.style.display = 'block';
			legendOpenButton.style.display = 'none';
		}
		legendCloseButton.onclick = function( ) {
			legend.style.display = 'none';
			legendOpenButton.style.display = 'block';
		}
	}

}

google.maps.event.addDomListener( window, 'load', initialize );
