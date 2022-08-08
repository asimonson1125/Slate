document.getRootNode().onkeyup = keyboardWatch;

function addParticipant() {
    let participants = document.getElementsByClassName('participants')[0];
    const length = participants.getElementsByClassName("box").length;
    let lastBox = participants.getElementsByClassName("box")[length - 1];
    let clone = document.getElementById('templateManual').content.cloneNode(true);
    clone.querySelector('.urlIn').name += length + 1;
    clone.querySelector('.nameIn').name += length + 1;
    clone.querySelector('.scoreIn').name += length + 1;
    clone.querySelector('.deleteManual').setAttribute('onclick', `deleteButton(${length})`);
    document.getElementsByClassName("participants")[0].appendChild(clone);
    placeholderNames();
}

function deleteButton(index) {
    let participants = document.getElementsByClassName("participants")[0];
    const participant = participants.children[index];
    participants.removeChild(participant);
    participants = document.getElementsByClassName("participants")[0];
    for (let i = index; i < participants.children.length; i++) {
        participants.children[i].children[0].children[1].name = "Calendar " + (i + 1);
        participants.children[i].children[1].children[1].name = "Name " + (i + 1);
        participants.children[i].children[2].children[1].name = "Score " + (i + 1);
        participants.children[i].children[3].setAttribute('onclick', `deleteButton(${i})`);
    }
    placeholderNames();
}

function placeholderNames() {
    let participants = document.getElementsByClassName("participants")[0].children;
    for (let i = 0; i < participants.length; i++) {
        participants[i].children[1].querySelector('textarea').placeholder = "Calendar #" + (i + 1);
    }
}

function keyboardWatch() { // trigger on keyup
    const e = document.activeElement;
    if (e.parentElement.className.includes("subBox")) {
        const lines = e.value.split("\n");
        if (lines.length > 1) {
            const name = e.getAttribute("name").split(" ")[0];
            let wherePut = e;
            wherePut.value = lines[0];
            for (let i = 1; i < lines.length; i++) {
                let nextBox = wherePut.parentElement.parentElement.nextElementSibling;
                if (nextBox === null) {
                    addParticipant();
                    nextBox = wherePut.parentElement.parentElement.nextElementSibling;
                }
                wherePut = null;
                for (let subBox = 0; subBox < nextBox.children.length; subBox++) {
                    if (nextBox.children[subBox].querySelector('textarea').getAttribute("name").includes(name)) {
                        wherePut = nextBox.children[subBox].querySelector('textarea');
                        break;
                    }
                }
                wherePut.value = lines[i];
            }
        }
    }
}