function makeLabels() {
    let table = document.getElementsByTagName('tr');
    let headers = document.getElementsByClassName("rowLabel");
    for (let i = 0; i < headers.length; i += 2) {
        try {
            let text = null;
            try {
                text = table[i + 1].children[1].children[0].children[0].children[0].children[0].textContent;
            } catch { text = table[i + 1].children[2].children[0].children[0].children[0].children[0].textContent; }
            if (text != null) {
                let substr = text.substring(text.indexOf('-') + 2, text.indexOf(" to"));
                headers[i].innerHTML = `<p>${substr}</p>`;
            }
        } catch { }
    }
    table = document.getElementsByTagName('tr');
    headers = document.querySelector("tbody > tr:nth-child(1)");
    for (let i = 1; i < headers.children.length; i++) {
        let text = null;
        row = 1;
        while (text == null) {
            try {
                text = table[row].children[i].children[0].children[0].children[0].children[0].textContent;
            } catch { row++; }
        }
        if (text !== null) {
            let substr = text.substring(0, 3);
            headers.children[i].innerHTML = `<p>${substr}</p>`;
        }

    }
}

function updateHighlights(){
    const inputs = document.querySelectorAll('#namesCheckbox > div > input');
    let names = [];
    for (let i = 0; i < inputs.length; i++){
        console.log(inputs[i].value, inputs[i].checked)
        if (inputs[i].checked){
            names.push(inputs[i].value);
        }
    }
    
    console.log("new highlight")
    names.forEach(function(x){console.log(x)})
    highlighter(names);
}

function highlighter(names){
    let boxes = document.querySelectorAll('.moreInfo > ul');
    // console.log("new highlight")
    // names.forEach(function(x){console.log(x)})

    if (names.length < 1){
        for (let box = 0; box < boxes.length; box++){
            boxes[box].parentElement.parentElement.parentElement.style.border = 'none';
        }
        return;
    }

    for (let box = 0; box < boxes.length; box++){
        let highlight = true;
        for(let i = 0; i < boxes[box].children.length; i++){
            let name = boxes[box].children[i].textContent;
            name = name.substring(0, name.lastIndexOf(', score:'));
            if(names.includes(name)){
                highlight = false;
                break;
            }
        }
        if(highlight){
            boxes[box].parentElement.parentElement.parentElement.style.border = 'solid grey 3px';
        }
        else{
            boxes[box].parentElement.parentElement.parentElement.style.border = 'none';
        }
    }

}

// to be implemented with highlighter
function highlightBest() {
    let scores = document.getElementsByClassName('score');
    let lowestScore = Number.MAX_SAFE_INTEGER;
    for (let i = 0; i < scores.length; i++) {
        let score = scores[i].innerText;
        score = parseInt(score.substring(7, score.indexOf('/') -1));
        if (lowestScore > score) { lowestScore = score;}
    }
    for (let i = 0; i < scores.length; i++){
        let score = scores[i].textContent;
        score = parseInt(score.substring(7, score.indexOf('/') -1));
        if (score == lowestScore){ // set parent td border color to white or sum
            scores[i].parentElement.parentElement.parentElement.style.border = 'solid yellow 2px';
        }
    }
}

// function highlightName(inName){
//     let unavailables = document.querySelectorAll('.moreInfo > ul');
//     for(let i = 0; i < unavailables.length; i++){
//         for(let j = 0; j < unavailables[i].children.length; j++){
//             let name = unavailables[i][j].textContent;
//             name = name.substring(0, egg.lastIndexOf(', score:'));
//             if(name == inName){
//                 unavailables[i].parentElement.parentElement.parentElement.style.border = 'solid grey 3px';
//             }
//         }
//     }
// }