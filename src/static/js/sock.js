let socket = io();

function emit(event){
    socket.emit(event);
}

function emitData(event, data){
    socket.emit(event, data)
}

socket.on('redirect', (dest) => {
    window.location.href = dest;
 });

 socket.on('loader', (status) => {
    loadStatus(status);
 }) 

 socket.on('loaded', (output) => {
    document.getElementById('container').innerHTML = output;
    document.getElementById('statusPopup').style.display = "none";
    makeLabels(); 
    dataSort();
 });