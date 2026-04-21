
var Isprimeiro = true

document.getElementById("send").addEventListener("click", function() {

    const input = document.getElementById("input").value;
    const msg = document.createElement("div");
    msg.classList.add("msg_sender");
    msg.textContent = input;
    document.getElementById("msg_input").appendChild(msg);
    document.getElementById("input").value = "";
    ConstruirMensagemResposta()
});


function ConstruirMensagemResposta(){
    const input = "Testes de mensagem"
    const msg = document.createElement("div");
    msg.classList.add("msg_receiver");
    msg.textContent = input;
    document.getElementById("msg_input").appendChild(msg);
    document.getElementById("input").value = "";
}