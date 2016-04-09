// Global map
var googleMap;
var markers = [];

// Socket
var socket = null;

// Other
var newTweets = 0;
var windowHasFocus = true;
var searchState = false;
var markerLifeTimeInHours = 1;


function clearMap(){
	for (var i = 0; i < markers.length; i++){
		markers[i].setMap(null);
	}
	markers = [];
}


function removeMarker(marker){
	marker.setMap(null);
	if (markers.indexOf(marker) >= 0)
		markers.splice(markers.indexOf(marker), 1);
}


function addMarker(position){
	var marker = new google.maps.Marker({
		position: position,
		map: googleMap,
		title: "Hendelse"
	});
	if (! searchState) marker.setAnimation(google.maps.Animation.BOUNCE);

	markers.push(marker);
	return marker;
}


function createTweetOnMap(id, position){
	
	var marker = addMarker(position);

	//Play sound when a new tweet arrives
	document.getElementById('notification-sound').play();

	// Disable bouncing after 20 sec.
	if (! searchState) setTimeout(function() { marker.setAnimation(null); }, 15000);

	// Create a info window to hold the tweet
	var infoWindow = new google.maps.InfoWindow({
		content: "<div class='info-window' id='" + id + "'><i class='fa fa-circle-o-notch fa-spin'></i></div>"
	});

	// Add a listener to the marker, opening the info window when clicked.
	marker.addListener('click', function() {
		marker.setAnimation(null);
		infoWindow.open(googleMap, marker);
		createTweet(id);
	});

	// If we are not in a search state give the marker a lifetime.
	if (! searchState) setTimeout(function() { removeMarker(marker); }, markerLifeTimeInHours * 3600000);
}


function createTweet(id){
	$('#' + id).html("<i class='fa fa-circle-o-notch fa-spin'></i>");
	twttr.widgets.createTweet(id, $('#' + id)[0]);
}


function initMap() {
	// Set map size equal to window size.
	var mapDiv =  $('#map');
	mapDiv.width($(window).width());
	mapDiv.height($(window).height());

	// Enable map
	googleMap = new google.maps.Map(mapDiv[0], {
		center: {lat: 65.1627612521667, lng: 17.149207687499953},
		zoom: 5
	});
}


function addTweet(id, position){
	createTweetOnMap(id, position);
}


function updateTitle(){
	if(windowHasFocus)
		document.title = "Norske politidistrikt - Twitter";
	else
		document.title = "(" + newTweets + ") Norske politidistrikt - Twitter" ;
}


// Web socket
$(document).ready(function (){
	var wsURI;

	if (window.location.protocol === "file:") {
		wsURI = "ws://localhost:9000";
	} else {
		wsURI = "ws://" + window.location.hostname + ":9000";
	}

	if ("WebSocket" in window) {
		socket = new WebSocket(wsURI);
	} else if ("MozWebSocket" in window) {
		socket = new MozWebSocket(wsURI);
	} else {
		log("Browser does not support WebSocket!");
		window.location = "http://autobahn.ws/unsupportedbrowser";
	}

	if (socket) {
		socket.onopen = function() {
			console.log("Connected to " + wsURI);
		};

		socket.onclose = function(e) {
			console.log("Connection closed (wasClean = " + e.wasClean + ", code = " + e.code + ", reason = '" + e.reason + "')");
			socket = null;
		};

		socket.onmessage = function(e) {
			var positionTweets = JSON.parse(e.data);
			for (var x in positionTweets['tweets']){
				addTweet(positionTweets['tweets'][x].id, positionTweets['tweets'][x].position);
			}

			if (! windowHasFocus)
				newTweets++;
			updateTitle();
		};
	}
});


function searchIsValid(){
	var startDate = $('input[name="start"]').val();
	var endDate = $('input[name="end"]').val();
	var searchString = $('input[name="query"]').val();

	if (startDate === ""){
		$('input[name="start"]').focus();
		return false;
	}
	else if (endDate === ""){
		$('input[name="end"]').focus();
		return false;
	}
	else if (searchString === ""){
		$('input[name="query"]').focus();
		return false;
	}
	else if (new Date(startDate) > new Date(endDate)){
		$('input[name="start"]').focus();
		return false;
	}
	return true;
}


// The following method can be used for searching
function search(msg) {
	clearMap();
	searchState = true;
	if (socket) {
		socket.send(msg);
		console.log("Sent: " + msg);
	} else {
		alert("Not connected, please refresh site.");
	}
}


function generateQueryObject(){
	return JSON.stringify({
		query: $('input[name="query"]').val(),
		startDate: $('input[name="start"]').val(),
		endDate: $('input[name="end"]').val()
	});
}


// Know when window has focus
$(window).focus(function() {
    windowHasFocus = true;
    newTweets = 0;
    updateTitle();
}).blur(function() {
    windowHasFocus = false;
});


$(document).ready(function(event) {
	// Listener on search
	$("form#search").submit(function( event ) {
		event.preventDefault();
		if (searchIsValid()){
			queryObject = generateQueryObject();
			search(queryObject);
		}
	});
});
