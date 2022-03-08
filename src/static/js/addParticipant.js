function addParticipant() {
    let lastBox = document.getElementsByClassName("box")[document.getElementsByClassName("box").length - 1];
    let clone = lastBox.cloneNode(true);
    document.getElementsByClassName("participants")[0].appendChild(clone);
}