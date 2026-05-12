const messages = document.getElementById("messages");
const input = document.getElementById("input");
const sendButton = document.getElementById("send");

let loading = false;

/* ================= SEND EVENTS ================= */

sendButton.addEventListener("click", sendMessage);

input.addEventListener("keyup", (event) => {

    if(event.key === "Enter"){
        sendMessage();
    }

});

/* ================= LOGIN ================= */

document
.getElementById("loginBtn")
.addEventListener("click", () => {

    document.getElementById("loginModal").style.display = "none";

});

/* ================= SEND MESSAGE ================= */

async function sendMessage(){

    if(loading) return;

    const text = input.value.trim();

    if(!text) return;

    removeWelcome();

    createMessage(text, "user");

    input.value = "";

    loading = true;

    createTyping();

    try{

        const response = await fetchAPI(text);

        removeTyping();

        createMessage(response, "bot");

    }catch(error){

        removeTyping();

        createMessage(
            "Erro ao conectar com a API.",
            "bot"
        );

        console.error(error);

    }

    loading = false;

}

/* ================= CREATE MESSAGE ================= */

function createMessage(text, type){

    const message = document.createElement("div");

    message.classList.add("message", type);

    message.innerHTML = text;

    messages.appendChild(message);

    scrollBottom();

}

/* ================= WELCOME ================= */

function removeWelcome(){

    const welcome = document.querySelector(".welcome");

    if(welcome){

        welcome.remove();

    }

}

/* ================= TYPING ================= */

function createTyping(){

    const typing = document.createElement("div");

    typing.classList.add("message", "bot");

    typing.id = "typing";

    typing.innerHTML = "Digitando...";

    messages.appendChild(typing);

    scrollBottom();

}

function removeTyping(){

    const typing = document.getElementById("typing");

    if(typing){

        typing.remove();

    }

}

/* ================= SCROLL ================= */

function scrollBottom(){

    messages.scrollTop = messages.scrollHeight;

}

/* ================= API ================= */

async function fetchAPI(message){

    const response = await fetch(
        `http://127.0.0.1:5000/sendmensage/API/${encodeURIComponent(message)}`
    );

    const data = await response.json();

    let formattedData = "";

    Object.keys(data.Response.dados).forEach((key) => {

        formattedData += `
            <strong>${key}</strong>: ${data.Response.dados[key]} <br>
        `;

    });

    return `
        <strong>Ação:</strong> ${data.Response.acao}<br><br>
        ${formattedData}
        <br>
        <strong>Sentimento:</strong> ${data.Response.sentimento}
    `;

}