document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const quickButtons = document.querySelectorAll('.quick-btn');
    
    function addMessage(content, isUser) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.innerHTML = `<p>${content}</p>`;
        
        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.textContent = getCurrentTime();
        
        messageDiv.appendChild(contentDiv);
        messageDiv.appendChild(timeDiv);
        
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    function getCurrentTime() {
        const now = new Date();
        return `${now.getHours()}:${now.getMinutes().toString().padStart(2, '0')}`;
    }
    
    function sendMessage() {
        const message = userInput.value.trim();
        if (message === '') return;
        
        addMessage(message, true);
        userInput.value = '';
        
        const typingIndicator = document.createElement('div');
        typingIndicator.className = 'message bot-message';
        typingIndicator.innerHTML = `
            <div class="message-content">
                <p><i class="fas fa-ellipsis-h"></i></p>
            </div>
        `;
        chatMessages.appendChild(typingIndicator);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        setTimeout(() => {
            chatMessages.removeChild(typingIndicator);
      
            fetch('/get_response', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message }),
            })
            .then(response => response.json())
            .then(data => {
                addMessage(data.response, false);
            })
            .catch(error => {
                console.error('Error:', error);
                addMessage("Sorry, I'm having trouble connecting. Please try again later.", false);
            });
        }, 1000);
    }
    
    sendButton.addEventListener('click', sendMessage);
    
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    quickButtons.forEach(button => {
        button.addEventListener('click', function() {
            userInput.value = this.getAttribute('data-question');
            sendMessage();
        });
    });
    
    const timeDivs = document.querySelectorAll('.message-time');
    timeDivs.forEach(div => {
        div.textContent = getCurrentTime();
    });
});