document.getRootNode().onkeyup = keyboardWatch;

function addParticipant() {
    let lastBox = document.getElementsByClassName("box")[document.getElementsByClassName("box").length - 1];
    let clone = lastBox.cloneNode(true);
    clone.children[0].children[1].value = "";
    clone.children[1].children[1].value = "";
    clone.children[2].children[1].value = 1;
    document.getElementsByClassName("participants")[0].appendChild(clone);
}

function keyboardWatch() { // trigger on keyup
    const e = document.activeElement;
    if (e.parentElement.className.includes("subBox")) {
        const lines = e.value.split("\n");
        if(lines.length > 1){
            const name = e.getAttribute("name");
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
                    if(nextBox.children[subBox].children[1].getAttribute("name") == name){
                        wherePut = nextBox.children[subBox].children[1];
                        break;
                    }
                }
                wherePut.value = lines[i];
            }            
        }
    }
}