function togglePassword() {

    const password =
        document.getElementById("password");

    if(password.type === "password") {

        password.type = "text";

    } else {

        password.type = "password";
    }
}

function copyPassword() {

    const password =
        document.getElementById("generatedPassword").innerText;

    navigator.clipboard.writeText(password);

    alert("Password copied!");
}
window.onclick = function(event) {

    const sidebar =
        document.getElementById(
            "sidebar"
        );

    const menuBtn =
        document.getElementById(
            "menuBtn"
        );

    if (
        !sidebar.contains(event.target)
        &&
        event.target !== menuBtn
    ) {
        sidebar.classList.remove(
            "active"
        );
    }
}

function toggleBreachPassword() {

    let password =
        document.getElementById(
            "breachPassword"
        );

    if (password.type === "password") {

        password.type = "text";

    } else {

        password.type = "password";

    }
}

function applyTheme(){

    let mode =
        localStorage.getItem(
            "sentinelMode"
        ) || "dark";

    let accent =
        localStorage.getItem(
            "sentinelAccent"
        ) || "green";

    document.body.classList.remove(
        "dark-theme",
        "light-theme",
        "green-theme",
        "blue-theme",
        "purple-theme"
    );

    document.body.classList.add(
        mode + "-theme"
    );

    document.body.classList.add(
        accent + "-theme"
    );
}

function setMode(mode){

    localStorage.setItem(
        "sentinelMode",
        mode
    );

    applyTheme();
}

function setAccent(accent){

    localStorage.setItem(
        "sentinelAccent",
        accent
    );

    applyTheme();
}

window.onload = function(){

    applyTheme();
}