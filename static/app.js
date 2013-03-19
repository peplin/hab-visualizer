WEB_SOCKET_SWF_LOCATION = "/static/WebSocketMain.swf";
WEB_SOCKET_DEBUG = true;

// socket.io specific code
var socket = io.connect('/track');

var path;
var pathHead;
var map;
var ourPathHead;

$(window).bind("beforeunload", function() {
    socket.disconnect();
});

socket.on('connect', function () {
    socket.emit('connect');
});

socket.on('position', function (latitude, longitude, altitude) {
    pathHead.setLatLng([latitude, longitude]);
    path.addLatLng(pathHead.getLatLng());
    // map.fitBounds(path.getBounds());
});

socket.on('reconnect', function () {
    $('#records').remove();
    message('System', 'Reconnected to the server');
});

socket.on('reconnecting', function () {
    message('System', 'Attempting to re-connect to the server');
});

socket.on('error', function (e) {
    message('System', e ? e : 'A unknown error occurred');
});

function message (from, msg) {
    $('#records').append($('<p>').append($('<b>').text(from), msg));
}

$(document).ready(function() {
    var startingPosition = new L.LatLng(39.970806, -119.387054);
    map = L.map('map').setView(startingPosition, 13);
    L.tileLayer('http://localhost:5000/static/images/tiles/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 18
    }).addTo(map);
    // L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        // attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
        // maxZoom: 14
    // }).addTo(map);
    //

    ourPath = L.polyline([], {color: 'blue'}).addTo(map);
    ourPathHead = L.marker(startingPosition).addTo(map);
    // create a red polyline from an arrays of LatLng points
    path = L.polyline([], {color: 'red'}).addTo(map);
    pathHead = L.circle(startingPosition, 100).addTo(map);

    $("#our_latitude").val(ourPathHead.getLatLng().lat);
    $("#our_longitude").val(ourPathHead.getLatLng().lng);
    $("#our_location").submit(function(e) {
        e.preventDefault();
        ourPathHead.setLatLng([
                parseFloat($("#our_latitude").val()),
                parseFloat($("#our_longitude").val()),
            ]);
        ourPath.addLatLng(ourPathHead.getLatLng());
        return false;
    });
});
