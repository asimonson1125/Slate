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
        member.querySelector('img').src = memberList[i]['image'];
        member.querySelector('img').alt = memberList[i]['name'];
        for(let x = 0; x < memberList[i]['groups'].length; x++){
            let group = document.getElementById('templateGroup').content.cloneNode(true);
            group.querySelector('p').textContent = memberList[i]['groups'][x];
            member.querySelector('.selectBox-groups').appendChild(group);
        }
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