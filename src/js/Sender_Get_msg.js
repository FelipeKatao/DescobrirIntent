
var Isprimeiro = true

document.getElementById("send").addEventListener("click", function() {
    if(Isprimeiro){
        document.getElementById("welcome").classList.add("bye")
        let a = setInterval(() => {
            document.getElementById("welcome").remove()
            ConstruirMensagem()
            clearInterval(a)
        }, 1000);
        Isprimeiro = false
    }
    else{
        ConstruirMensagem()
    }

});


function ConstruirMensagem(){
    const input = document.getElementById("input").value;
    const msg = document.createElement("div");
    msg.classList.add("msg_sender");
    msg.textContent = input;
    document.getElementById("msg_input").appendChild(msg);
    document.getElementById("input").value = "";
    ConstruirMensagemResposta()
}

function ConstruirMensagemResposta(){
    const input = "Testes de mensagem"
    const msg = document.createElement("div");
    msg.classList.add("msg_receiver");
    msg.textContent = input;
    document.getElementById("msg_input").appendChild(msg);
    document.getElementById("input").value = "";
}