function validateForm(){
    let calCount = 1;
    let url = document.forms["slateIn"][`Calendar 1`];
    while(url != undefined){
        if(url.value.length < 4){
            alert(`Missing URL data for calendar #${calCount}`);
            return false;
        }
        if(document.forms["slateIn"][`Score ${calCount}`].value == ''){
            alert(`Missing score for calendar #${calCount}`);
            return false;
        }
        calCount++
        url = document.forms["slateIn"][`Calendar ${calCount}`];
        
    }
    const start = Number(new Date(document.forms["slateIn"]["startTime"].value));
    const end = Number(new Date(document.forms["slateIn"]["endTime"].value));
    if(!(start > 1) || !(end > 1)){
        alert("start/end dates must have a day and time");
        return false;
    }
    if(start >= end){
        alert("Start time must be before end time");
        return false;
    }
    const duration = document.forms["slateIn"]["duration"].value;
    const interval = document.forms["slateIn"]["interval"].value;
    if(duration < 15 || duration > 1440){
        alert("Duration must be between 15 minutes and 1440 minutes (2 hours)");
        return false;
    }
    if(interval < 15 || interval > 1440){
        alert("Interval must be between 15 minutes and 1440 minutes (2 hours)");
        return false;
    }
}