// import { emitData } from "./sock.js"

function validateForm() {
    let calCount = 1;
    let url = document.forms["slateIn"][`Calendar 1`];
    while (url != undefined) {
        if (url.value.length < 4) {
            alert(`Missing URL data for calendar #${calCount}`);
            return false;
        }
        if (document.forms["slateIn"][`Score ${calCount}`].value == '') {
            alert(`Missing score for calendar #${calCount}`);
            return false;
        }
        calCount++
        url = document.forms["slateIn"][`Calendar ${calCount}`];

    }
    const start = Number(new Date(document.forms["slateIn"]["startTime"].value));
    const end = Number(new Date(document.forms["slateIn"]["endTime"].value));
    if (!(start > 1) || !(end > 1)) {
        alert("start/end dates must have a day and time");
        return false;
    }
    if (start >= end) {
        alert("Start time must be before end time");
        return false;
    }
    const duration = document.forms["slateIn"]["duration"].value;
    const interval = document.forms["slateIn"]["interval"].value;
    if (duration < 15 || duration > 1440) {
        alert("Duration must be between 15 minutes and 1440 minutes (2 hours)");
        return false;
    }
    if (interval < 15 || interval > 1440) {
        alert("Interval must be between 15 minutes and 1440 minutes (2 hours)");
        return false;
    }
}

function submitForm() {
    const form = document.querySelector('form');
    const data = new FormData(form).entries();
    const urls = [];
    const names = [];
    const scores = [];
    let info = data.next().value
    while(info[0] !== "utc-offset"){
        urls.push(info[1]);
        info = data.next().value
        if(info[1] === ""){
            info = info[0];
        }
        else{
            info = "Unnamed" + info[1].substring(indexOf(" "));
        }
        names.push(info);
        scores.push(parseInt(data.next().value[1]));
        info = data.next().value;
    }
    const timezone = info[1];
    info = data.next().value;
    let DSTtick = false;
    if(info[0] === "daylightSavingsTick"){
        DSTtick = true;
        info = data.next().value;
    }
    const interval =  info[1];
    const start = data.next().value[1];
    const end = data.next().value[1];
    const length = data.next().value[1];

    const submission = [urls, names, scores, timezone, start, end, DSTtick, interval, length]
    emitData('submit', submission)
}