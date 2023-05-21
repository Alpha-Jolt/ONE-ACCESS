const form = document.getElementById("form")
const username = document.getElementById("username")
const fingerDiv = document.getElementById("fingerprint-verification")

form.addEventListener("submit", (e)=>{
        e.preventDefault();
        username.value =  "";
        
        fingerDiv.classList.add("show-finger")
})