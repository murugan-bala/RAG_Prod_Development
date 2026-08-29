const loginForm = document.getElementById("loginForm");
const loginMessage = document.getElementById("loginMessage");

loginForm.addEventListener("submit", async function (event) {

    event.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    try {

        const response = await fetch("http://127.0.0.1:8000/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });

        const data = await response.json();

        if (data.success) {

            localStorage.setItem("username", data.username);

            loginMessage.textContent = "Login successful!";
            loginMessage.style.color = "green";

            setTimeout(function () {
                window.location.href = "chat.html";
            }, 500);

        } else {

            loginMessage.textContent = data.message;
            loginMessage.style.color = "red";
        }

    } catch (error) {

        console.error("Login error:", error);

        loginMessage.textContent =
            "Cannot connect to FastAPI server.";

        loginMessage.style.color = "red";
    }
});