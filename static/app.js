WEB_SOCKET_SWF_LOCATION = "/static/WebSocketMain.swf";
WEB_SOCKET_DEBUG = true;

// socket.io specific code
var socket = io.connect('/track');

var path;
var map;

$(window).bind("beforeunload", function() {
    socket.disconnect();
});

socket.on('connect', function () {
    socket.emit('connect');
});

socket.on('position', function (latitude, longitude, altitude) {
    path.addLatLng([latitude, longitude]);
    map.fitBounds(path.getBounds());
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
    map = L.map('map').setView([40.0245, -118.936], 13);
    // L.tileLayer('http://localhost:5000/static/tiles/tile1.png', {
        // maxZoom: 18
    // }).addTo(map);
    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 14
    }).addTo(map);

    var marker = L.marker([40.0245, -118.936]).addTo(map);
    // create a red polyline from an arrays of LatLng points
    path = L.polyline([], {color: 'red'}).addTo(map);
});
