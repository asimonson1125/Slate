function toggleDropdown(e){
    e.classList.toggle("show");
}

dropdowns = document.querySelectorAll(".dropdown-toggle");
for(let i = 0; i < dropdowns.length; i++){
    let e = dropdowns[i].nextElementSibling;
    dropdowns[i].onclick = function (){toggleDropdown(e) };
}