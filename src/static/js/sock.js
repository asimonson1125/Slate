let socket = io();

function emit(event) {
   socket.emit(event);
}

function emitData(event, data) {
   socket.emit(event, data)
}

function ayylmao(string){
   if(string.startsWith('urlCheck')){
      checkResults(string.substring(8));
   }
   else{
      alert(string);
   }
}

socket.on('redirect', (dest) => {
   window.location.href = dest;
});

socket.on('stringtype', (string) => {
   ayylmao(string);
});

socket.on('loader', (status) => {
   loadStatus(status);
});

socket.on('memberList', (members) => {
   loadMembers(members);
});

socket.on('loaded', (output) => {
   const results = document.getElementById('results');
   results.innerHTML = output;
   document.getElementById('views').scrollIntoView(false);
   document.querySelector('#statusPopup').style.display = 'none';
   makeLabels();
   dataSort();
   analysis();
   scrollToElement(results);
});

socket.on('loadUpdate', (index) => {
   let list = document.getElementById('calendarStatus');
   list.children[index].querySelector('.progressBar').style.backgroundColor = "lightgray";
});