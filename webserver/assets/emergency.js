// Global map
var map;

// Socket
var socket = null;

// Other
var newTweets = 0;
var windowHasFocus = true;

function getTweet(id, position){
	$.getJSON({
		dataType: "jsonp",
		url: "https://api.twitter.com/1/statuses/oembed.json",
		data: {
			id: id,
			omit_script: true
		},
		success: function(tweet){
			placeTweetOnMap(position, tweet, id);
		}
	});
}

function placeTweetOnMap(id, position){
	var marker = new google.maps.Marker({
		position: position,
		map: map,
		title: "Hendelse",
		animation: google.maps.Animation.BOUNCE
	});

	//Play sound when a new tweet arrives
	document.getElementById('notification-sound').play();

	// Disable bouncing after 20 sec.
	setTimeout(function() { marker.setAnimation(null); }, 20000);

	// Create a info window to hold the tweet
	var infoWindow = new google.maps.InfoWindow({
		content: "<div id='" + id + "'></div>"
	});

	// Add a listener to the marker, opening the info window when clicked.
	marker.addListener('click', function() {
		marker.setAnimation(null);
		infoWindow.open(map, marker);
		createTweet(id);
	});
}

function createTweet(id){
	$('#' + id).html("");
	twttr.widgets.createTweet(id, $('#' + id)[0]);
}


function initMap() {
	// Set map size equal to window size.
	var mapDiv =  $('#map');
	mapDiv.width($(window).width());
	mapDiv.height($(window).height());

	// Enable map
	map = new google.maps.Map(mapDiv[0], {
		center: {lat: 65.908857, lng: 14.380653},
		zoom: 5
	});
}

function addTweet(id, position){
	placeTweetOnMap(id, position);
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
			var positionTweet = JSON.parse(e.data);
			addTweet(positionTweet.id, positionTweet.position);

			if (! windowHasFocus)
				newTweets++;
			updateTitle();
		};
	}

	// The following method can be used for searching
	function search(msg) {
		if (socket) {
			socket.send(msg);
			console.log("Sent: " + msg);
		} else {
			console.log("Not connected.");
		}
	}
});

// Know when window has focus
$(window).focus(function() {
    windowHasFocus = true;
    newTweets = 0;
    updateTitle();
}).blur(function() {
    windowHasFocus = false;
});
