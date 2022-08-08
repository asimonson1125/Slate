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
function loadMembers(members){
    memberList = members;
    let container = document.getElementById('memberSearchScroll');
    while(container.children > 0){
        container.removeChild(container.children[0]);
    }
    for(let i = 0; i < memberList.length; i++){
        let member = document.getElementById('templateMember').content.cloneNode(true);
        member.querySelector('h4').textContent = memberList[i]['name'];
        member.querySelector('p').textContent = memberList[i]['uid'];
        member.querySelector('img').src = 'https://profiles.csh.rit.edu/image/' + memberList[i]['uid'];
        member.querySelector('img').alt = memberList[i]['name'];
        member.id = 'member ' + i;
        container.appendChild(member);
    }
}

function searchForMembers(){
    let searchParams = document.getElementById('searchMembers').value.toLowerCase();
    let members = document.getElementsByClassName('selectBox');
    for(let i = 0; i < members.length; i++){
        let name = members[i].querySelector('h4').textContent.toLowerCase();
        let user = members[i].querySelector('p').textContent.toLowerCase();
        if(name.includes(searchParams) || user.includes(searchParams)){
            members[i].classList.remove('hidden');
            console.log("revealed " + name);
        }
        else{
            members[i].classList.add('hidden');
        }
    }
}