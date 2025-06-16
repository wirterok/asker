document.getElementById('chat-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    const input = document.getElementById('message-input');
    const text = input.value.trim();
    if (!text) return;
    input.value = '';
    
    // Add question to chat
    const messagesDiv = document.getElementById('messages');
    const questionDiv = document.createElement('div');
    questionDiv.className = 'message question';
    questionDiv.textContent = text;
    messagesDiv.appendChild(questionDiv);
    messagesDiv.appendChild(document.createElement('div')).className = 'clearfix';
    messagesDiv.scrollTop = messagesDiv.scrollHeight;

    // Send question to backend
    console.log("here")
    const response = await fetch('/api/message/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: text })
    });
    const data = await response.json();

    // Add answer to chat
    const answerDiv = document.createElement('div');
    answerDiv.className = 'message answer';
    answerDiv.textContent = data.content;
    messagesDiv.appendChild(answerDiv);
    messagesDiv.appendChild(document.createElement('div')).className = 'clearfix';
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
});