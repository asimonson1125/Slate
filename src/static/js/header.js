function toggleDropdown(i){
    document.querySelectorAll(".dropdown-menu")[i].classList.toggle("show")
}

let dropdowns = document.querySelectorAll(".dropdown-toggle");
for(let i = 0; i < dropdowns.length; i++){
    dropdowns[i].onclick = function (){toggleDropdown(i) };
}