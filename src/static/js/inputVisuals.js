function startForm() {
    today = new Date();
    let month = today.getMonth() + 1;
    if (month < 10) month = '0' + month;
    let day = today.getDate();
    if (day < 10) day = '0' + day;
    let hour = today.getHours();
    if (hour < 10) hour = '0' + hour;

    document.getElementsByName("startTime")[0].value = today.getFullYear() + "-" + month + "-" + day + "T" + hour + ":00";

    today.setDate(today.getDate() + 7)
    month = today.getMonth() + 1;
    if (month < 10) month = '0' + month;
    day = today.getDate();
    if (day < 10) day = '0' + day;
    hour = today.getHours();
    if (hour < 10) hour = '0' + hour;
    document.getElementsByName("endTime")[0].value = today.getFullYear() + "-" + month + "-" + day + "T" + hour + ":00";
}

let memberList = [];
let selectedMembers = [];
function loadMembers(members) {
    memberList = members;
    let container = document.getElementById('memberSearchScroll');
    while (container.children > 0) {
        container.removeChild(container.children[0]);
    }
    for (let i = 0; i < memberList.length; i++) {
        let member = document.getElementById('templateMember').content.cloneNode(true);
        member.querySelector('.selectBox').setAttribute('onclick', `selectMember(${i})`);
        member.querySelector('h4').textContent = memberList[i]['name'];
        member.querySelector('p').textContent = memberList[i]['uid'];
        member.querySelector('img').src = memberList[i]['image'];
        member.querySelector('img').alt = memberList[i]['name'];
        for (let x = 0; x < memberList[i]['groups'].length; x++) {
            let group = document.getElementById('templateGroup').content.cloneNode(true);
            group.querySelector('p').textContent = memberList[i]['groups'][x];
            member.querySelector('.selectBox-groups').appendChild(group);
        }
        member.id = 'member ' + i;
        container.appendChild(member);
    }
    document.getElementById('loadingMembers').style.display = 'none';
    updateSearchScroll();
}

function searchForMembers() {
    let searchParams = document.getElementById('searchMembers').value.toLowerCase();
    let members = document.getElementsByClassName('selectBox');
    for (let i = 0; i < members.length; i++) {
        let name = members[i].querySelector('h4').textContent.toLowerCase();
        let user = members[i].querySelector('p').textContent.toLowerCase();
        if (name.includes(searchParams) || user.includes(searchParams)) {
            members[i].classList.remove('hidden');
        }
        else {
            members[i].classList.add('hidden');
        }
    }
}

function selectMember(index) {
    let members = document.getElementById('memberSearchScroll').children;
    if (!selectedMembers.includes(index)) {
        selectedMembers.push(index);
    }
    else {
        selectedMembers = selectedMembers.filter(e => e != index);
    }
    updateSelection();
}

function updateSelection() {
    const template = document.getElementById('templateSelection').content;
    let display = document.getElementById('selectedParticipants');
    let current = document.querySelectorAll('#selectedParticipants > .selection');
    for (let i = 0; i < current.length; i++) {
        if (!selectedMembers.includes(parseInt(current[i].id.substring(10)))) {
            display.removeChild(current[i]);
        }
    }
    for (let i = 0; i < selectedMembers.length; i++) {
        if (document.getElementById('selection ' + selectedMembers[i]) == null) {
            let selected = template.cloneNode(true);
            selected.querySelector('.selection').id = "selection " + selectedMembers[i];
            selected.querySelector('img').src = memberList[selectedMembers[i]]['image'];
            selected.querySelector('img').alt = memberList[selectedMembers[i]]['name'];
            selected.querySelector('.nameDisplay').textContent = memberList[selectedMembers[i]]['name'];
            selected.querySelector('.urlDisplay').textContent = "[super secret]";
            selected.querySelector('.delete').setAttribute('onclick', `removeSelection('selection ${selectedMembers[i]}')`);
            display.appendChild(selected);
        }
    }
    updateStatus();
    checkHeader();
}

function updateStatus() {
    let members = document.getElementsByClassName('selectBox');
    for (let i = 0; i < members.length; i++) {
        if (selectedMembers.includes(i)) {
            members[i].classList.add('selected');
        }
        else {
            members[i].classList.remove('selected');
        }
    }
}

function removeSelection(id) {
    document.getElementById(id).parentElement.removeChild(document.getElementById(id));
    if (id.includes('selection')) {
        selectedMembers = selectedMembers.filter(e => e != parseInt(id.substring(10)));
        updateStatus();
    }
    else {
        idAdjust();
    }
}

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
        participants[i].querySelector('.nameDisplay').placeholder = "Unnamed #" + (i + 1);
        participants[i].querySelector('.delete').setAttribute('onclick', `removeSelection("${'manual ' + (i + 1)}")`);
        participants[i].id = 'manual ' + (i + 1);
    }
    checkHeader();
}

function selectAll() {
    let all = document.getElementsByClassName('selectBox');
    let visible = [];
    for (let i = 0; i < all.length; i++) {
        if (!all[i].classList.contains('hidden')) {
            visible.push(all[i]);
        }
    }
    let allSelected = true;
    for (let i = 0; i < visible.length; i++) {
        if (!visible[i].classList.contains('selected')) {
            allSelected = false;
            break;
        }
    }
    if (allSelected) {
        for (let i = 0; i < visible.length; i++) {
            visible[i].classList.remove('selected');
            const index = Array.from(visible[i].parentNode.children).indexOf(visible[i]);
            selectedMembers = selectedMembers.filter(e => e != index);
        }
    }
    else {
        for (let i = 0; i < visible.length; i++) {
            if (!visible[i].classList.contains('selected')) {
                visible[i].classList.add('selected');
                const index = Array.from(visible[i].parentNode.children).indexOf(visible[i]);
                selectedMembers.push(index);
            }
        }
    }
    updateSelection();
}

function checkHeader() {
    if (document.getElementsByClassName('selection').length > 0) {
        document.getElementById('inHeaders').classList.remove('hidden');
    }
    else {
        document.getElementById('inHeaders').classList.add('hidden');
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
                options[i + x].value = lines[x];
            }
        }
    }
}

function updateSearchScroll() {
    let scrolls = document.getElementsByClassName('scroller');
    for (let i = 0; i < scrolls.length; i++) { // ideally there's only ever one, but just to be safe...
        let current = scrolls[i].scrollLeft;
        let max = scrolls[i].scrollLeftMax;
        let parent = scrolls[i].parentElement;
        let maxArrow = parent.querySelector('.maxArrow');
        let minArrow = parent.querySelector('.minArrow');
        if(current < max){
            maxArrow.classList.remove('invisible');
        }
        else{
            maxArrow.classList.add('invisible');
        }
        if(current >= 2){
            minArrow.classList.remove('invisible');
        }
        else{
            minArrow.classList.add('invisible');
        }
    }
}