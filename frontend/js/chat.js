console.log("chat.js loaded");

const questionInput = document.getElementById("questionInput");
const sendButton = document.getElementById("sendButton");
const chatMessages = document.getElementById("chatMessages");
const logoutButton = document.getElementById("logoutButton");

const username = localStorage.getItem("username");

if (!username) {
    window.location.href = "login.html";
}


// Send button
sendButton.addEventListener("click", function () {
    sendQuestion();
});


// Press Enter to send
questionInput.addEventListener("keydown", function (event) {

    if (event.key === "Enter") {

        event.preventDefault();

        sendQuestion();
    }
});


// Send question to FastAPI
async function sendQuestion() {

    const question = questionInput.value.trim();

    if (question === "") {
        return;
    }

    console.log("Sending question:", question);

    // Show user message
    addMessage(question, "user");

    // Clear input
    questionInput.value = "";

    // Disable button
    sendButton.disabled = true;

    // Show thinking message
    const thinkingMessage = addMessage(
        "Thinking...",
        "bot"
    );

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/chat",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    username: username,
                    question: question
                })
            }
        );

        if (!response.ok) {
            throw new Error(
                "Server returned status " + response.status
            );
        }

        const data = await response.json();

        console.log("Response:", data);

        // Remove thinking message
        thinkingMessage.remove();

        // Show answer
        addMessage(
            data.answer,
            "bot"
        );

    } catch (error) {

        console.error(
            "Chat error:",
            error
        );

        thinkingMessage.remove();

        addMessage(
            "Unable to connect to the server.",
            "bot"
        );
    }

    // Enable button
    sendButton.disabled = false;

    // Focus input again
    questionInput.focus();
}


// Add message to chat
function addMessage(message, type) {

    const messageDiv =
        document.createElement("div");

    if (type === "user") {

        messageDiv.className =
            "user-message";

    } else {

        messageDiv.className =
            "bot-message";
    }

    messageDiv.textContent = message;

    chatMessages.appendChild(
        messageDiv
    );

    chatMessages.scrollTop =
        chatMessages.scrollHeight;

    return messageDiv;
}


// Logout
logoutButton.addEventListener(
    "click",
    function () {

        const confirmLogout =
            confirm("Do you want to logout?");

        if (confirmLogout) {

            localStorage.removeItem(
                "username"
            );

            localStorage.removeItem(
                "token"
            );

            window.location.href =
                "login.html";
        }
    }
);