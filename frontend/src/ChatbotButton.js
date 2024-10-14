import React, { useState } from 'react';
import './ChatbotButton.css'; 

function ChatbotButton() {
    const [showChat, setShowChat] = useState(false);
    const [messages, setMessages] = useState([]); // Store chat messages
    const [newMessage, setNewMessage] = useState(""); // Store input text

    const handleClick = () => {
        setShowChat(true);
    };

    const handleClose = () => {
        setShowChat(false);
    };

    const handleSendMessage = (e) => {
        e.preventDefault();
        if (newMessage.trim() !== "") {
            setMessages([...messages, { text: newMessage, sender: 'user' }]);
            setNewMessage("");
            setTimeout(() => {
                const chatBody = document.querySelector(".chat-body");
                chatBody.scrollTop = chatBody.scrollHeight;
            }, 100);
        }
    };

    return (
        <div>
            <button
                className="chatbot-button"
                onClick={handleClick}
            >
                <img src="/chatbot.png" alt="Chatbot" />
            </button>

            {showChat && (
                <div className="chat-popup">
                    <div className="chat-header">
                        <button onClick={handleClose}>Close</button>
                    </div>
                    <div className="chat-body">
                        {messages.map((message, index) => (
                            <div key={index} className={`message-bubble ${message.sender}`}>
                                {message.text}
                            </div>
                        ))}
                    </div>
                    <div className="chat-footer">
                        <form onSubmit={handleSendMessage}>
                            <input
                                type="text"
                                value={newMessage}
                                onChange={(e) => setNewMessage(e.target.value)}
                                placeholder="Type a message..."
                                className="chat-input"
                            />
                            <button type="submit" className="send-button">Send</button>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
}

export default ChatbotButton;
