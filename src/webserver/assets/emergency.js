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


function enterSearchState(){
	searchState = true;
	for (var i = 0; i < markers.length; i++){
		markers[i].setMap(null);
	}
	markers = [];
	$('.tweet-list').hide();
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

	// Disable bouncing after 20 sec.
	if (! searchState) setTimeout(function() { marker.setAnimation(null); }, 15000);

	// Create a info window to hold the tweet
	var infoWindow = new google.maps.InfoWindow({
		content: "<i class='fa fa-circle-o-notch fa-spin'></i><div style='display: none' class='info-window' id='" + id + "'></div>"
	});

	// Add a listener to the marker, opening the info window when clicked.
	marker.addListener('click', function() {
		marker.setAnimation(null);
		infoWindow.open(googleMap, marker);
		createPositionalTweet(id);
	});

	infoWindow.addListener('closeclick', function(){
		this.setContent("<i class='fa fa-circle-o-notch fa-spin'></i><div style='display: none' class='info-window' id='" + id + "'></div>");
	});

	// If we are not in a search state give the marker a lifetime.
	if (! searchState) setTimeout(function() { removeMarker(marker); }, markerLifeTimeInHours * 3600000);
}


function createPositionalTweet(id){
	twttr.widgets.createTweet(id, $('#' + id)[0]).then(function(el){
		$('i.fa-circle-o-notch').hide();
		$('#' + id).show();
	});
}


function createListTweet(id){
	$('#list').prepend($('<div id="' + id + '"></div>'));
	twttr.widgets.createTweet(id, $('#' + id)[0], {width: 350, align: "center"});
}


function initMap() {
	// Set map size equal to window size.
	var mapDiv =  $('#map');
	mapDiv.width($(window).width());
	mapDiv.height($(window).height());

	// Enable map
	googleMap = new google.maps.Map(mapDiv[0], {
		center: {lat: 65.1627612521667, lng: 23.609168624999953},
		zoom: 5
	});

	// Resize map when window resizes
	google.maps.event.addDomListener(window, "resize", function() {
		var center = googleMap.getCenter();
		mapDiv.width($(window).width());
		mapDiv.height($(window).height());
		google.maps.event.trigger(googleMap, "resize");
		googleMap.setCenter(center);
	});
}


function addPositionalTweet(id, position){
	createTweetOnMap(id, position);
}


function addTweetToList(id){
	$(".tweet-list").show();
	createListTweet(id);
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
			var tweets = JSON.parse(e.data);
			for (var x in tweets['tweets']){
				if (typeof tweets['tweets'][x].position !== 'undefined')
					addPositionalTweet(tweets['tweets'][x].id, tweets['tweets'][x].position);
				else
					addTweetToList(tweets['tweets'][x].id);
			}

			if (! windowHasFocus)
				newTweets++;
			updateTitle();

			//Play sound when a new tweet arrives
			document.getElementById('notification-sound').play();
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
function search(query) {
	enterSearchState();
	if (socket) {
		socket.send(query);
		console.log("Sent: " + query);
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

	// Default date today
	$('input[name="start"], input[name="end"]').val(new Date().toDateInputValue());
});


Date.prototype.toDateInputValue = (function() {
    var local = new Date(this);
    local.setMinutes(this.getMinutes() - this.getTimezoneOffset());
    return local.toJSON().slice(0,10);
});
