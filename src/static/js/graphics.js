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