// Global map
var googleMap;
var markers = [];
var openInfoWindow = null;

// Socket
var socket = null;

// Other
var newTweets = 0;
var windowHasFocus = true;
var searchState = false;
var markerLifeTimeInHours = 1;

// Selected categories
var selectedEvidence = false;
var selectedEvent = false;


function enterSearchState(){
	searchState = true;
	for (var i = 0; i < markers.length; i++){
		markers[i].setMap(null);
	}
	markers = [];
	$('.tweet-list').hide();
	disableSearchForm();
}


function removeMarker(marker){
	marker.setMap(null);
	if (markers.indexOf(marker) >= 0)
		markers.splice(markers.indexOf(marker), 1);
}


function addMarker(position){
	var latlng = new google.maps.LatLng(position);

	//final position for marker, could be updated if another marker already exists in same position
	var finalLatLng = latlng;

	//check to see if any of the existing markers match the latlng of the new marker
	if (markers.length !== 0) {
		for (i=0; i < markers.length; i++) {
			var existingMarker = markers[i];
			var pos = existingMarker.getPosition();

			//if a marker already exists in the same position as this marker
			if (latlng.equals(pos)) {
				//update the position of the coincident marker by applying a small multipler to its coordinates
				var newLat = latlng.lat() + (Math.random() -0.5) / 60;// * (Math.random() * (max - min) + min);
				var newLng = latlng.lng() + (Math.random() -0.5) / 30;// * (Math.random() * (max - min) + min);
				finalLatLng = new google.maps.LatLng(newLat,newLng);
			}
		}
	}
	var marker = new google.maps.Marker({
		position: finalLatLng,
		map: googleMap,
		title: "Tweet"
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
		if(openInfoWindow !== null){
			google.maps.event.trigger(openInfoWindow, 'closeclick');
			openInfoWindow.close();
		}
		marker.setAnimation(null);
		infoWindow.open(googleMap, marker);
		openInfoWindow = infoWindow;
		createPositionalTweet(id);
	});

	infoWindow.addListener('closeclick', function(){
		clearInfoWindow(infoWindow, id);
	});

	// If we are not in a search state give the marker a lifetime.
	if (! searchState) setTimeout(function() { removeMarker(marker); }, markerLifeTimeInHours * 3600000);
}

function clearInfoWindow(infoWindow, id){
	infoWindow.setContent("<i class='fa fa-circle-o-notch fa-spin'></i><div style='display: none' class='info-window' id='" + id + "'></div>");
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

			if (searchState){
				$('.search-result').show();
				$('.search-result .hits').html(tweets['tweets'].length);
				enableSearchForm();
			}

			//Play sound when new tweets arrives
			if (tweets['tweets'].length) document.getElementById('notification-sound').play();
		};
	}
});


function searchIsValid(){
	var startDate = $('#search input[name="start"]').val();
	var endDate = $('#search input[name="end"]').val();
	var searchString = $('i#search nput[name="query"]').val();

	if (startDate === ""){
		$('#search input[name="start"]').focus();
		return false;
	}
	else if (endDate === ""){
		$('#search input[name="end"]').focus();
		return false;
	}
	else if (searchString === ""){
		$('#search input[name="query"]').focus();
		return false;
	}
	else if (new Date(startDate) > new Date(endDate)){
		$('#search input[name="start"]').focus();
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


function generateSearchQueryObject(){
	return JSON.stringify({
		query: $('#search input[name="query"]').val(),
		startDate: $('#search input[name="start"]').val(),
		endDate: $('#search input[name="end"]').val(),
		type: 'search'
	});
}


function generateCategoryQueryObject(){
	if(selectedEvent || selectedEvidence){
		return JSON.stringify({
			event: selectedEvent,
			evidence: selectedEvidence,
			startDate: $('#category input[name="start"]').val(),
			endDate: $('#category input[name="end"]').val(),
			type: 'category'
		});
	}
	else {
		alert("Vennligst velg minimun en artifakt eller en hendelse.");
		return false;
	}
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
			queryObject = generateSearchQueryObject();
			search(queryObject);
		}
	});

	// Listener on category search
	$("form#category").submit(function( event ) {
		event.preventDefault();
		queryObject = generateCategoryQueryObject();
		if (queryObject)
			search(queryObject);
	});

	// Default date today
	$('input[name="start"], input[name="end"]').val(new Date().toDateInputValue());

	// Click listeners on category buttons
	$('.category-buttons .evidence i').click(function(){
		var currentId  = $('.category-buttons .evidence i.selected').attr('id');
		$('.category-buttons .evidence i').removeClass('selected');
		if ($(this).attr('id') == selectedEvidence)
			selectedEvidence = false;
		else{
			$(this).addClass('selected');
			selectedEvidence = $(this).attr('id');
		}
	});

	$('.category-buttons .events i').click(function(){
		var currentId  = $('.category-buttons .events i.selected').attr('id');
		$('.category-buttons .events i').removeClass('selected');
		if ($(this).attr('id') == selectedEvent)
			selectedEvent = false;
		else{
			$(this).addClass('selected');
			selectedEvent = $(this).attr('id');
		}
	});

	// Change from search to categories and back
	$('.toggle-button').click(function(){
		$('.option-box').toggleClass('active-search');
	});

	// Listeners to coordinate dates.
	$('#search input[name="start"]').change(function(){
		$('#category input[name="start"]').val($(this).val());
	});

	$('#search input[name="end"]').change(function(){
		$('#category input[name="end"]').val($(this).val());
	});

	$('#category input[name="start"]').change(function(){
		$('#search input[name="start"]').val($(this).val());
	});

	$('#category input[name="end"]').change(function(){
		$('#search input[name="end"]').val($(this).val());
	});
});


function enableSearchForm(){
	$('.search-loader').hide();
	$('.search-button').show();
}


function disableSearchForm(){
	$('.search-button').hide();
	$('.search-loader').show();
}


Date.prototype.toDateInputValue = (function() {
    var local = new Date(this);
    local.setMinutes(this.getMinutes() - this.getTimezoneOffset());
    return local.toJSON().slice(0,10);
});
