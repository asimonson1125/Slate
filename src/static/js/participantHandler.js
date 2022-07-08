document.getRootNode().onkeyup = keyboardWatch;

function addParticipant() {
    const length = document.getElementsByClassName("box").length;
    let lastBox = document.getElementsByClassName("box")[length - 1];
    let clone = lastBox.cloneNode(true);
    clone.children[0].children[1].value = "";
    clone.children[0].children[1].name = "Calendar " + (length + 1);
    clone.children[1].children[1].value = "";
    clone.children[1].children[1].name = "Name " + (length + 1);
    clone.children[2].children[1].value = 1;
    clone.children[2].children[1].name = "Score " + (length + 1);
    clone.children[3].setAttribute('onclick',`deleteButton(${length})`);
    document.getElementsByClassName("participants")[0].appendChild(clone);
    placeholderNames()
}

function removeParticipant(){
    const length  = document.getElementsByClassName("box").length - 1;
    if(length == 0){
        alertNotEnoughParticipants();
        return;
    }
    let lastBox = document.getElementsByClassName("box")[length];
    lastBox.parentElement.removeChild(lastBox);
}

function deleteButton(index){
    let participants = document.getElementsByClassName("participants")[0];
    if(participants.children.length <= 1){
        alertNotEnoughParticipants();
        return;
    }
    const participant = participants.children[index];
    participants.removeChild(participant);
    participants = document.getElementsByClassName("participants")[0];
    for(let i = index; i < participants.children.length; i++){
        participants.children[i].children[0].children[1].name = "Calendar " + (i + 1);
        participants.children[i].children[1].children[1].name = "Name " + (i + 1);
        participants.children[i].children[2].children[1].name = "Score " + (i + 1);
        participants.children[i].children[3].setAttribute('onclick',`deleteButton(${i})`);
    }
    placeholderNames()
}

function placeholderNames(){
    let participants = document.getElementsByClassName("participants")[0].children;
    for (let i = 0; i < participants.length; i++){
        participants[i].children[1].querySelector('textarea').placeholder = "Calendar #" + (i+1);
    }
}

function alertNotEnoughParticipants(){
    alert("Minimum of 1 participant required");
}

function keyboardWatch() { // trigger on keyup
    const e = document.activeElement;
    if (e.parentElement.className.includes("subBox")) {
        const lines = e.value.split("\n");
        if(lines.length > 1){
            const name = e.getAttribute("name").split(" ")[0];
            let wherePut = e;
            wherePut.value = lines[0];
            for (let i = 1; i < lines.length; i++) {
                let nextBox = wherePut.parentElement.parentElement.nextElementSibling;
                if(nextBox === null){
                    addParticipant();
                    nextBox = wherePut.parentElement.parentElement.nextElementSibling;
                }
                wherePut = null;
                for(let subBox = 0; subBox < nextBox.children.length; subBox++){
                    if(nextBox.children[subBox].querySelector('textarea').getAttribute("name").includes(name)){
                        wherePut = nextBox.children[subBox].querySelector('textarea');
                        break;
                    }
                }
                wherePut.value = lines[i];
            }            
        }
    }
}