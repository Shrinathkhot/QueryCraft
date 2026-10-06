const messageInput = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");
const chatMessages = document.getElementById("chatMessages");
const typingContainer = document.getElementById("typingContainer");


async function sendMessage() {

    const message = messageInput.value.trim();

    if (!message) {
        return;
    }

    // Add user message
    addUserMessage(message);

    // Clear input
    messageInput.value = "";

    // Reset textarea height
    messageInput.style.height = "auto";

    // Disable button
    sendButton.disabled = true;

    // Show typing indicator
    showTyping();


    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })

        });


        const data = await response.json();


        hideTyping();


        if (data.success) {

            addBotMessage(data.response);

        } else {

            addBotMessage(
                "Error: " + data.error
            );

        }

    } catch (error) {

        hideTyping();

        addBotMessage(
            "Unable to connect to the QueryCraft server. Please make sure Flask is running."
        );

        console.error(error);

    }


    sendButton.disabled = false;

    messageInput.focus();
}



function addUserMessage(message) {

    const messageElement =
        document.createElement("div");

    messageElement.className =
        "message user-message";


    messageElement.innerHTML = `

        <div class="avatar">
            YOU
        </div>

        <div class="message-content">

            <div class="message-name">
                Question
            </div>

            <div class="message-bubble">
                ${escapeHTML(message)}
            </div>

        </div>

    `;


    chatMessages.appendChild(messageElement);

    scrollToBottom();
}


function addBotMessage(message) {

    const messageElement =
        document.createElement("div");

    messageElement.className =
        "message bot-message";


    const formattedMessage =
        formatBotResponse(message);


    messageElement.innerHTML = `

        <div class="avatar">
            AI
        </div>

        <div class="message-content">

            <div class="message-name">
                QueryCraft
            </div>

            <div class="message-bubble">
                ${formattedMessage}
            </div>

        </div>

    `;


    chatMessages.appendChild(messageElement);

    scrollToBottom();
}


function formatBotResponse(text) {

    return marked.parse(text);

}


function showTyping() {

    typingContainer.style.display = "flex";

    scrollToBottom();
}


function hideTyping() {

    typingContainer.style.display = "none";
}


function scrollToBottom() {

    setTimeout(() => {

        chatMessages.scrollTop =
            chatMessages.scrollHeight;

    }, 50);
}


function escapeHTML(text) {

    const div =
        document.createElement("div");

    div.textContent = text;

    return div.innerHTML;
}


messageInput.addEventListener(
    "keydown",
    function(event) {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            sendMessage();

        }

    }
);


messageInput.addEventListener(
    "input",
    function() {

        this.style.height = "auto";

        this.style.height =
            Math.min(
                this.scrollHeight,
                120
            ) + "px";

    }
);


sendButton.addEventListener(
    "click",
    sendMessage
);