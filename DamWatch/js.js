const login_btn=document.querySelector("#login-btn")
const signup_btn=document.querySelector("#signup-btn")
const container=document.querySelector(".container")

signup_btn.addEventListener("click", () => {
    container.classList.add("sign-up-mode");
})
login_btn.addEventListener("click", () => {
    container.classList.remove("sign-up-mode");
})
