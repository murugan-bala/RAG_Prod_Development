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


// Enter key
questionInput.addEventListener("keyup", function (event) {

    if (event.key === "Enter") {
        sendQuestion();
    }

});


// Send question
async function sendQuestion() {

    const question = questionInput.value.trim();

    if (question === "") {
        return;
    }

    addMessage(question, "user");

    questionInput.value = "";

    sendButton.disabled = true;

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

        thinkingMessage.remove();

        // Show answer
        addMessage(
            data.answer,
            "bot"
        );

        // Show PDF sources
        if (data.sources && data.sources.length > 0) {

            addSources(data.sources);
        }

    } catch (error) {

        console.error("Chat error:", error);

        thinkingMessage.remove();

        addMessage(
            "Unable to connect to the server.",
            "bot"
        );
    }

    sendButton.disabled = false;

    questionInput.focus();
}


// Add normal chat message
function addMessage(message, type) {

    const messageDiv =
        document.createElement("div");

    if (type === "user") {
        messageDiv.className = "user-message";
    } else {
        messageDiv.className = "bot-message";
    }

    messageDiv.textContent = message;

    chatMessages.appendChild(messageDiv);

    chatMessages.scrollTop =
        chatMessages.scrollHeight;

    return messageDiv;
}


// Add PDF source names
function addSources(sources) {

    const sourceDiv =
        document.createElement("div");

    sourceDiv.className = "source-message";

    const title =
        document.createElement("strong");

    title.textContent = "Sources:";

    sourceDiv.appendChild(title);


    const uniqueFiles = [];

    sources.forEach(function (source) {

        if (!uniqueFiles.includes(source.file_name)) {

            uniqueFiles.push(source.file_name);
        }
    });


    uniqueFiles.forEach(function (fileName) {

        const fileDiv =
            document.createElement("div");

        fileDiv.textContent =
            "📄 " + fileName;

        sourceDiv.appendChild(fileDiv);
    });


    chatMessages.appendChild(sourceDiv);

    chatMessages.scrollTop =
        chatMessages.scrollHeight;
}


// Logout
logoutButton.addEventListener(
    "click",
    function () {

        const confirmLogout =
            confirm("Do you want to logout?");

        if (confirmLogout) {

            localStorage.removeItem("username");

            localStorage.removeItem("token");

            window.location.href =
                "login.html";
        }
    }
);