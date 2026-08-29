console.log("chat.js loaded");

const questionInput = document.getElementById("questionInput");
const sendButton = document.getElementById("sendButton");
const chatMessages = document.getElementById("chatMessages");
const logoutButton = document.getElementById("logoutButton");

console.log("questionInput:", questionInput);
console.log("sendButton:", sendButton);
console.log("chatMessages:", chatMessages);

const username = localStorage.getItem("username");

console.log("Username:", username);

if (!username) {
window.location.href = "login.html";
}

// SEND BUTTON
sendButton.addEventListener("click", function () {


console.log("SEND BUTTON CLICKED");

const question = questionInput.value.trim();

console.log("Question:", question);

if (question === "") {
    alert("Please enter a question");
    return;
}

sendQuestion(question);


});

// SEND QUESTION
async function sendQuestion(question) {


console.log("sendQuestion() started");

try {

    console.log("About to call FastAPI...");

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

    console.log("FastAPI response received");
    console.log("Status:", response.status);

    const data = await response.json();

    console.log("Response data:", data);

    addMessage(question, "user");
    addMessage(data.answer, "bot");

    questionInput.value = "";

} catch (error) {

    console.error("ERROR:", error);

    alert("Error: " + error.message);
}


}

// ADD MESSAGE
function addMessage(message, type) {


const messageDiv = document.createElement("div");

if (type === "user") {
    messageDiv.className = "user-message";
} else {
    messageDiv.className = "bot-message";
}

messageDiv.textContent = message;

chatMessages.appendChild(messageDiv);

chatMessages.scrollTop = chatMessages.scrollHeight;


}

// LOGOUT
logoutButton.addEventListener("click", function () {


if (confirm("Do you want to logout?")) {

    localStorage.removeItem("username");
    localStorage.removeItem("token");

    window.location.href = "login.html";
}


});
