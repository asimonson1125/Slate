function startForm() {
    today = new Date();
    let month = today.getMonth();
    if (month < 10) month = '0' + month;
    let day = today.getDate();
    if (day < 10) day = '0' + day;
    let hour = today.getHours();
    if (hour < 10) hour = '0' + hour;
    
    document.getElementsByName("startTime")[0].value = today.getFullYear() + "-" + month + "-" + day + "T" + hour + ":00";

    today.setDate(today.getDate() + 7)
    month = today.getMonth();
    if (month < 10) month = '0' + month;
    day = today.getDate();
    if (day < 10) day = '0' + day;
    hour = today.getHours();
    if (hour < 10) hour = '0' + hour;
    document.getElementsByName("endTime")[0].value = today.getFullYear() + "-" + month + "-" + day + "T" + hour + ":00";
}

// function expandableParticipants() {
//     document
// }

