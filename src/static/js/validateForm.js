// import { emitData } from "./sock.js"

function validateForm() {
    const participants = document.querySelectorAll('#manualParticipants > .selection');
    const all = document.getElementsByClassName('selection');
    const form = document.forms["slateIn"];
    if (all.length == 0) {
        alert("Select or add at least 1 participant!");
        return false;
    }
    for (let i = 0; i < participants.length; i++) {
        if (participants[i].querySelector('.urlDisplay').value.length < 4) {
            alert(`Missing URL data for manually added calendar #${i}`);
            return false;
        }
    }
    for (let i = 0; i < all.length; i++) {
        let score;
        score = parseInt(all[i].querySelector('.finalScore').value);
        if (isNaN(score) || !Number.isInteger(score) || score < -1) {
            alert("Score must be an integer >= -1.");
            return false;
        }
    }

    const start = Number(new Date(form["startTime"].value));
    const end = Number(new Date(form["endTime"].value));
    if (!(start > 1) || !(end > 1)) {
        alert("start/end dates must have a day and time");
        return false;
    }
    if (start >= end) {
        alert("Start time must be before end time");
        return false;
    }
    const duration = form["duration"].value;
    const interval = form["interval"].value;
    if (duration < 15 || duration > 1440) {
        alert("Duration must be between 15 minutes and 1440 minutes (2 hours)");
        return false;
    }
    if (interval < 15 || interval > 1440) {
        alert("Interval must be between 15 minutes and 1440 minutes (2 hours)");
        return false;
    }
    return true;
}

function submitForm() {
    let urls = [], names = [], scores = [], type = [];
    const members = document.querySelectorAll('#selectedParticipants > .selection');
    for (let i = 0; i < members.length; i++) {
        let selected = selectedMembers[i];
        uid = memberList[selected]['uid'];
        if (memberList[selected]['type'] == 'example') {
            type.push('manual');
            urls.push(memberList[selected]['icallink'])
        }
        else {
            type.push(memberList[selected]['type']);
            urls.push(uid);
        }
        names.push(members[i].querySelector('.nameDisplay').textContent);
        scores.push(parseInt(members[i].querySelector('.finalScore').value));
    }

    const manual = document.querySelectorAll('#manualParticipants > .selection');
    for (let i = 0; i < manual.length; i++) {
        let name = manual[i].querySelector('.nameDisplay').value;
        if (name == '') {
            name = manual[i].querySelector('.nameDisplay').placeholder;
        }
        urls.push(manual[i].querySelector('.urlDisplay').value);
        names.push(name);
        scores.push(parseInt(manual[i].querySelector('.finalScore').value));
        type.push('manual')
    }

    const form = document.forms["slateIn"];
    const ignoreErrors = form['ignoreErrors'].checked;
    const timezone = form["utc-offset"].value;
    const DSTtick = form["daylightSavingsTick"].checked;
    const duration = form["duration"].value;
    const interval = form["interval"].value;
    const start = form["startTime"].value;
    const end = form["endTime"].value;

    const submission = [urls, names, scores, type, ignoreErrors, timezone, start, end, DSTtick, interval, duration]
    emitData('submit', submission)
}