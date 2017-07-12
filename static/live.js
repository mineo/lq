var socket = new WebSocket("ws://localhost:9000");
socket.onmessage = function(e) {
    var payload = JSON.parse(e.data);
    var message = payload.user + ": " + payload.message;

    var li = document.createElement("li");
    var span = document.createElement("span");
    span.appendChild(document.createTextNode(message));
    li.appendChild(span);
    var ul = document.getElementById("live-messages");
    ul.appendChild(li);
};