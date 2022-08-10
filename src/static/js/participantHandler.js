document.getRootNode().onkeyup = keyboardWatch;

function addParticipant() {
    let participants = document.getElementById('manualParticipants');
    const length = participants.children.length;
    let clone = document.getElementById('templateManual').content.cloneNode(true);
    clone.querySelector('.selection').id += 'manual ' + (length + 1);
    clone.querySelector('.delete').setAttribute('onclick', `removeSelection("${'manual ' + (length + 1)}")`);
    participants.appendChild(clone);
    idAdjust();
}

function idAdjust() {
    let participants = document.querySelectorAll("#manualParticipants > .selection");
    for (let i = 0; i < participants.length; i++) {
        participants[i].querySelector('.nameDisplay').placeholder = "Calendar #" + (i + 1);
        participants[i].querySelector('.delete').setAttribute('onclick', `removeSelection("${'manual ' + (i + 1)}")`);
        participants[i].id = 'manual ' + (i + 1);
    }
}

function keyboardWatch() { // trigger on keyup
    const e = document.activeElement;
    let type = 'none';
    if (e.className.includes("nameDisplay")) {
        type = 'nameDisplay';
    }
    else if (e.className.includes("urlDisplay")) {
        type = 'urlDisplay';
    }
    else if (e.className.includes("finalScore")) {
        type = 'finalScore';
    }
    if (type != 'none') {
        const lines = e.value.split("\n");
        if (lines.length > 1) {
            let options = document.getElementsByClassName(type);
            let i = 0;
            while (options[i] != e) { i++; }
            for (let x = 0; x < lines.length; x++) {
                if (options.length == i + x) {
                    addParticipant();
                    options = document.getElementsByClassName(type);
                }
                console.log(i, options)
                options[i + x].value = lines[x];
            }
        }
    }
}