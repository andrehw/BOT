
document.getElementById('send-btn').addEventListener('click', sendMessage);
document.getElementById('user-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') sendMessage();
});



async function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    if (!message) return;

    // 1. Mostrar mensaje del usuario en pantalla
    addMessage(message, 'user');
    input.value = '';

    // 2. Enviar a Django
    try {
        const response = await fetch('/api/chat/', { // Asegúrate que esta URL coincida con tu urls.py
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken') // Importante para la seguridad de Django
            },
            body: `message=${encodeURIComponent(message)}`
        });

        const data = await response.json();
        addMessage(data.reply, 'bot');
    } catch (error) {
        addMessage("Error de conexión con el servidor.", 'bot');
    }
}

function addMessage(text, sender) {
    const chatWindow = document.getElementById('chat-window');
    const msgDiv = document.createElement('div');
    msgDiv.innerText = text;
    
    // Estilos rápidos según el remitente
    if (sender === 'user') {
        
        msgDiv.style.cssText = "background: #007bff; color: white; padding: 8px 12px; border-radius: 15px; align-self: flex-end; max-width: 80%;";
    } else {

        msgDiv.style.cssText = "background: #e1e1e1; color: black; padding: 8px 12px; border-radius: 15px; align-self: flex-start; max-width: 80%;";
        }
    
    chatWindow.appendChild(msgDiv);


    if (sender !== 'user' && text.has_file && text.file_metadata) {
        const meta = text.file_metadata;
        const tarjetaArchivo = document.createElement('div');
        tarjetaArchivo.style.cssText = "align-self: flex-start; max-width: 80%; margin-bottom: 8px;";
        tarjetaArchivo.innerHTML = `
            <div style="border: 1px solid #214f81; padding: 12px; border-radius: 8px; margin-top: 8px; display: flex; align-items: center; gap: 10px; background: #f4f4f4;">
                <span style="font-size: 24px;">📄</span>
                <div>
                    <h3>${meta.bot_response}</h3>
                    <strong style="display: block; color: #333;">${meta.display_name}</strong>
                    <a href="${meta.download_url}" download="${meta.file_name}" target="_blank" style="color: #214f81; font-weight: bold; text-decoration: none;">Descargar PDF</a>
                </div>
            </div>
        `;
        chatWindow.appendChild(tarjetaArchivo);


    }

    chatWindow.scrollTop = chatWindow.scrollHeight; // Auto-scroll al final
}

// Función auxiliar para el token CSRF de Django
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


let headChat = document.querySelector('#chat-header')
let chat = document.querySelector('.section-chat')

function mostrarChat(){

    chat.classList.toggle("active");
};
headChat.addEventListener("click", mostrarChat);