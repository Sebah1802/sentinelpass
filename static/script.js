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