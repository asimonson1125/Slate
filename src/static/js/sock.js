let socket = io();

function emit(event){
    console.log("sending event: " + event);
    socket.emit(event, {data: '\n\nI\'m connected!\n\n'});
}

socket.on('redirect', (dest) => {
    window.location.href = dest;
 });