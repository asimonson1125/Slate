let socket = io();

function emit(event){
    socket.emit(event);
    console.log("sent event: " + event);
}

socket.on('redirect', (dest) => {
    window.location.href = dest;
 });

 socket.on('loaded', (output) => {
    document.getElementById('container').innerHTML = output;
 });