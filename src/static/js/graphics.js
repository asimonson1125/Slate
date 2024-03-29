function makeLabels() {
    /**
     * makes headers for datatables
     */
    let t = document.getElementById('timescroll');
    let table = t.querySelectorAll('tr');
    let headers = t.getElementsByClassName("rowLabel");
    for (let i = 0; i < headers.length; i += 2) {
        try {
            let text = null;
            try {
                text = table[i + 1].children[1].querySelector('h3').textContent;
            } catch { text = table[i + 1].children[2].querySelector('h3').textContent; }
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
                text = table[row].children[i].querySelector('h3').textContent;
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
    /**
     * Highlights timeslots
     */
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
    /**
     * highlights timeslots if they contain names
     */
    let boxes = document.getElementById('timescroll').querySelectorAll('.cell');

    for (let box = 0; box < boxes.length; box++) {
        let list = boxes[box].querySelectorAll('li');
        let highlight = true;
        for (let i = 0; i < list.length; i++) {
            let name = list[i].textContent;
            name = name.substring(0, name.lastIndexOf(', score:'));
            if (names.includes(name)) {
                highlight = false;
                break;
            }
        }
        if (highlight) {
            boxes[box].parentElement.style.opacity = '1';
        }
        else {
            boxes[box].parentElement.style.opacity = '.6';
        }
    }

}

// to be implemented with highlighter
// function highlightBest() {
//     let scores = document.getElementById('timescroll').getElementsByClassName('score');
//     let lowestScore = Number.MAX_SAFE_INTEGER;
//     for (let i = 0; i < scores.length; i++) {
//         let score = scores[i].innerText;
//         score = parseInt(score.substring(7, score.indexOf('/') - 1));
//         if (lowestScore > score) { lowestScore = score; }
//     }
//     for (let i = 0; i < scores.length; i++) {
//         let score = scores[i].textContent;
//         score = parseInt(score.substring(7, score.indexOf('/') - 1));
//         if (score == lowestScore) { // set parent td border color to white or sum
//             scores[i].parentElement.parentElement.parentElement.style.border = 'solid yellow 2px';
//         }
//     }
// }


let months = [];
let month = 0;
function dataSort() {
    /**
     * breaks data into month periods
     */
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
        let button = document.createElement('p');
        button.textContent = months[i][0];
        button.addEventListener('click', () => { selectMonth(i) })
        views.appendChild(button);
    }
    views.childNodes[0].classList.add('selectedView');
}

function selectMonth(number) {
    /**
     * makes data from target month visible
     */
    let data = document.querySelectorAll('#timescroll > tbody > tr');
    let views = document.querySelectorAll('#views > p');
    for (let i = 0; i < views.length; i++) {
        views[i].classList.remove('selectedView');
    }
    views[number].classList.add('selectedView');
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
    /**
     * loading popup updater
     */
    console.log("FUCK")
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
            let cal = document.getElementById('templateProgress').content.cloneNode(true);
            cal.querySelector('.calStatus').textContent = status[i][0];
            // .progressBar  => style.backgroundColor = "rgba(0, 0, 0, 0)";
            cal.querySelector('.progress').style.width = status[i][1];
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

function scrollToElement(e) {
    /**
     * scroll to element with header offset
     */
    const headerOffset = 65;
    let elementPosition = e.offsetTop;
    var offsetPosition = elementPosition - headerOffset;
    window.scrollTo({
        top: offsetPosition,
        behavior: "smooth"
    });
}