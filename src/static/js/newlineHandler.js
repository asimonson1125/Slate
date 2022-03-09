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
    document.getElementsByClassName("participants")[0].appendChild(clone);
}

function removeParticipant(){
    const length  = document.getElementsByClassName("box").length - 1;
    if(length == 1){
        return;
    }
    let lastBox = document.getElementsByClassName("box")[length];
    lastBox.parentElement.removeChild(lastBox);
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
                    if(nextBox.children[subBox].children[1].getAttribute("name").includes(name)){
                        wherePut = nextBox.children[subBox].children[1];
                        break;
                    }
                }
                wherePut.value = lines[i];
            }            
        }
    }
}