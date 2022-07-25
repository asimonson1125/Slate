function makeLabels() {
    let t = document.getElementById('timescroll');
    let table = t.querySelectorAll('tr');
    let headers = t.getElementsByClassName("rowLabel");
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
    table = t.getElementsByTagName('tr');
    headers = t.querySelector("tbody > tr:nth-child(1)");
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
    updateHighlights();
}

function updateHighlights() {
    const inputs = document.querySelectorAll('#namesCheckbox > div > input');
    let names = [];
    for (let i = 0; i < inputs.length; i++) {
        if (inputs[i].checked) {
            names.push(inputs[i].value);
        }
    }
    highlighter(names);
}

function highlighter(names) {
    let boxes = document.getElementById('timescroll').querySelectorAll('.moreInfo > ul');

    for (let box = 0; box < boxes.length; box++) {
        let highlight = true;
        for (let i = 0; i < boxes[box].children.length; i++) {
            let name = boxes[box].children[i].textContent;
            name = name.substring(0, name.lastIndexOf(', score:'));
            if (names.includes(name)) {
                highlight = false;
                break;
            }
        }
        if (highlight) {
            boxes[box].parentElement.parentElement.parentElement.style.opacity = '1';
        }
        else {
            boxes[box].parentElement.parentElement.parentElement.style.opacity = '.6';
        }
    }

}

// to be implemented with highlighter
function highlightBest() {
    let scores = document.getElementById('timescroll').getElementsByClassName('score');
    let lowestScore = Number.MAX_SAFE_INTEGER;
    for (let i = 0; i < scores.length; i++) {
        let score = scores[i].innerText;
        score = parseInt(score.substring(7, score.indexOf('/') - 1));
        if (lowestScore > score) { lowestScore = score; }
    }
    for (let i = 0; i < scores.length; i++) {
        let score = scores[i].textContent;
        score = parseInt(score.substring(7, score.indexOf('/') - 1));
        if (score == lowestScore) { // set parent td border color to white or sum
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

let months = [];
let month = 0;

function dataSort() {
    let data = document.querySelectorAll('#timescroll > tbody > tr');
    let firstData;
    for (let i = 1; i < data.length; i++) {
        if (data[i].children[1].querySelector('.cell') !== null) {
            firstData = i;
            break;
        }
    }
    months = [];
    month = 0;
    let firstText = data[firstData].children[1].querySelector('.moreInfo > h3').textContent;
    firstText = firstText.substring(firstText.indexOf(',') + 2)
    firstText = firstText.substring(0, firstText.indexOf(' ')) + firstText.substring(firstText.indexOf(',') + 1, firstText.indexOf('-') - 1)
    months.push([firstText, 1, data[1].children.length]);
    for (let i = 2; i < data[1].children.length; i++) {
        let text = data[1].children[i].querySelector('.moreInfo > h3').textContent;
        text = text.substring(text.indexOf(',') + 2)
        text = text.substring(0, text.indexOf(' ')) + text.substring(text.indexOf(',') + 1, text.indexOf('-') - 1)
        if (text !== months[months.length - 1][0]) {
            months[months.length - 1][2] = i;
            months.push([text, i, data[1].children.length]);
        }
    }
    for (let i = months[0][2]; i < data[1].children.length; i++) {
        for (let j = 0; j < data.length; j++) {
            data[j].children[i].classList.add('hidden');
        }
    }

    let views = document.getElementById('views');
    for (let i = 0; i < months.length; i++) {
        let button = document.createElement('button');
        button.innerText = months[i][0];
        button.addEventListener('click', () => { selectMonth(i) })
        views.appendChild(button);
    }
}

function selectMonth(number) {
    let data = document.getElementById('timescroll').querySelectorAll('#hoverBox > tbody > tr');
    for (let i = 1; i < data[1].children.length; i++) {
        for (let j = 0; j < data.length; j++) {
            data[j].children[i].classList.add('hidden');
        }
    }
    for (let i = months[number][1]; i < months[number][2]; i++) {
        for (let j = 0; j < data.length; j++) {
            data[j].children[i].classList.remove('hidden');
        }
    }
}

function loadStatus(status) {
    let screen = document.querySelector('#statusPopup');
    let list = document.getElementById('calendarStatus');
    if (typeof status == 'string') {
        alert(status);
        screen.style.display = "none";
    }
    else if (screen.style.display !== "block") {
        // create screen
        while (list.lastChild) {
            list.removeChild(list.lastChild);
        }
        document.getElementById('totalbar').style.width = '0px';
        screen.style.display = "block";
        for (let i = 1; i < status.length; i++) {
            let cal = document.createElement('li');
            let div = document.createElement('div');
            let name = document.createElement('p');
            name.classList.add('calStatus')
            name.textContent = status[i][0];
            let loaded = document.createElement('div');
            loaded.classList.add("progressBar");
            loaded.style.backgroundColor = "rgba(0, 0, 0, 0)";
            let state = document.createElement('div');
            state.classList.add("progress");
            state.style.width = status[i][1];
            div.appendChild(name);
            loaded.appendChild(state);
            div.appendChild(loaded)
            cal.appendChild(div);
            list.appendChild(cal);
        }
    }
    else {
        for (let i = 1; i < status.length; i++) {
            // update status
            list.children[i - 1].querySelector('.progress').style.width = status[i][1] + 'px';
        }
    }
    document.getElementById('loadingtext').textContent = status[0][1];
    document.getElementById('totalbar').style.width = status[0][0] + '%';
}