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
    document.documentElement.innerHTML = output;
    makeLabels(); 
    dataSort();
 });

 socket.on('loadUpdate', (index) => {
    let list = document.getElementById('calendarStatus');
    list.children[index].querySelector('.progressBar').style.backgroundColor = "lightgray";
 })