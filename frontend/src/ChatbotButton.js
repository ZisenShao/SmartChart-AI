import React, { useState, useRef} from 'react';
import './ChatbotButton.css'; 

function ChatbotButton() {
    const [showChat, setShowChat] = useState(false);
    const [messages, setMessages] = useState([]); // Store chat messages
    const [newMessage, setNewMessage] = useState(""); // Store input text
    const [buttonPosition, setButtonPosition] = useState({ top: window.innerHeight - 120, left: window.innerWidth - 70 });
    const buttonRef = useRef(null);

    const handleClick = () => {
        setShowChat(true);
    };

    const handleClose = () => {
        setShowChat(false);
    };

    const handleMouseDown = (e) => {
        e.preventDefault();
        const initialX = e.clientX;
        const initialY = e.clientY;
        const initialButtonLeft = buttonPosition.left;
        const initialButtonTop = buttonPosition.top;

        const handleMouseMove = (moveEvent) => {
            const newX = initialButtonLeft + (moveEvent.clientX - initialX);
            const newY = initialButtonTop + (moveEvent.clientY - initialY);
            const pageWidth = window.innerWidth;
            const pageHeight = window.innerHeight;
            const buttonWidth = 50;
            const buttonHeight = 50;

            setButtonPosition({
                left: Math.min(Math.max(newX, 0), pageWidth - buttonWidth),
                top: Math.min(Math.max(newY, 0), pageHeight - buttonHeight),
            });
        };

        const handleMouseUp = () => {
            window.removeEventListener('mousemove', handleMouseMove);
            window.removeEventListener('mouseup', handleMouseUp);
        };

        window.addEventListener('mousemove', handleMouseMove);
        window.addEventListener('mouseup', handleMouseUp);
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
                onMouseDown={handleMouseDown}
                style={{ top: buttonPosition.top, left: buttonPosition.left, position: 'fixed' }} 
                ref={buttonRef}
            >
                <img src="/chatbot.png" alt="Chatbot" />
            </button>

            {showChat && (
                <div className="chat-popup" style={{ left: buttonPosition.left - 300, top: buttonPosition.top - 350 }}>
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
