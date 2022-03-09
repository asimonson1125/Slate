function makeLabels() {
    const table = document.getElementsByTagName('tr');
    let headers = document.getElementsByClassName("rowLabel");
    for (let i = 0; i < headers.length; i += 2) {
        try {
            let text = null;
            try {
                text = table[i].children[1].children[0].children[0].children[0].children[0].textContent;
            } catch { text = table[i].children[2].children[0].children[0].children[0].children[0].textContent; }
            if (text != null) {
                let substr = text.substring(text.indexOf('-') + 2, text.indexOf(" to"));
                headers[i].innerHTML = `<p>${substr}</p>`;
            }
        } catch { console.log("FUCK") }
    }
}