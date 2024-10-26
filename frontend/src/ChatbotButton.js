import React, { useState, useRef, useEffect } from 'react';
import { marked } from 'marked';
import './ChatbotButton.css';

function ChatbotButton() {
    const [showChat, setShowChat] = useState(false);
    const [messages, setMessages] = useState([]); // Store chat messages
    const [newMessage, setNewMessage] = useState(""); // Store input text
    const [buttonPosition, setButtonPosition] = useState({ top: window.innerHeight - 120, left: window.innerWidth - 70 });
    const [startPosition, setStartPosition] = useState({ top: window.innerHeight - 120, left: window.innerWidth - 70 });
    const [isAnimating, setIsAnimating] = useState(false);
    const [isDragging, setIsDragging] = useState(false);
    const buttonRef = useRef(null);
    const chatPopupRef = useRef(null);

    const popupWidth = 300;
    const popupHeight = 350;
    const buttonWidth = 60;
    const buttonHeight = 60;
    const margin = 10; // Margin from the edges of the screen

    useEffect(() => {
        updateChatPosition();
    }, [buttonPosition, showChat]);

    const toggleChat = () => {
        if (showChat) {
            setIsAnimating(true);
            setShowChat(false);
            setTimeout(() => {
                setButtonPosition(startPosition);
                setTimeout(() => setIsAnimating(false), 300); // Match this with the CSS transition duration
            }, 0);
        } else {
            setShowChat(true);
        }
    };

    const handleClose = () => {
        toggleChat();
    };

    const handleMouseDown = (e) => {
        if (isAnimating) return; // Prevent dragging during animation

        e.preventDefault();
        const initialX = e.clientX;
        const initialY = e.clientY;
        const initialButtonLeft = buttonPosition.left;
        const initialButtonTop = buttonPosition.top;

        let hasMoved = false;
        let dragThreshold = 5; // pixels

        const handleMouseMove = (moveEvent) => {
            const deltaX = Math.abs(moveEvent.clientX - initialX);
            const deltaY = Math.abs(moveEvent.clientY - initialY);

            if (deltaX > dragThreshold || deltaY > dragThreshold) {
                hasMoved = true;
                setIsDragging(true);
            }

            if (hasMoved) {
                const newX = initialButtonLeft + (moveEvent.clientX - initialX);
                const newY = initialButtonTop + (moveEvent.clientY - initialY);
                const pageWidth = window.innerWidth;
                const pageHeight = window.innerHeight;

                // Calculate the limits for button movement
                const minLeft = showChat ? (popupWidth + margin) : margin;
                const maxLeft = pageWidth - buttonWidth - margin;
                const minTop = showChat ? (popupHeight + margin) : margin;
                const maxTop = pageHeight - buttonHeight - margin;

                const newButtonPosition = {
                    left: Math.min(Math.max(newX, minLeft), maxLeft),
                    top: Math.min(Math.max(newY, minTop), maxTop),
                };

                setButtonPosition(newButtonPosition);
            }
        };

        const handleMouseUp = (upEvent) => {
            window.removeEventListener('mousemove', handleMouseMove);
            window.removeEventListener('mouseup', handleMouseUp);

            setIsDragging(false);

            if (!hasMoved) {
                toggleChat();
            }
        };

        window.addEventListener('mousemove', handleMouseMove);
        window.addEventListener('mouseup', handleMouseUp);
    };

    const updateChatPosition = () => {
        if (!showChat || !chatPopupRef.current) return;

        const pageWidth = window.innerWidth;
        const pageHeight = window.innerHeight;

        // Calculate chat position based on button position
        let popupLeft = buttonPosition.left - popupWidth;
        let popupTop = buttonPosition.top - popupHeight;

        // Ensure chat stays within screen bounds
        popupLeft = Math.max(margin, Math.min(popupLeft, pageWidth - popupWidth - margin));
        popupTop = Math.max(margin, Math.min(popupTop, pageHeight - popupHeight - margin));

        chatPopupRef.current.style.left = `${popupLeft}px`;
        chatPopupRef.current.style.top = `${popupTop}px`;
    };

    const handleSendMessage = async (e) => {
        e.preventDefault();
        if (newMessage.trim() !== "") {
            setMessages([...messages, { text: newMessage, sender: 'user' }]);
            setNewMessage("");
            //set POST request to backend
            try {
                const response = await fetch('http://localhost:8000/api/chat/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: newMessage }), //send the content of message
                });

                const data = await response.json();

                // deal with the response
                if (response.ok) {
                    setMessages(prevMessages => [...prevMessages, { text: data.message, sender: 'bot' }]);
                } else {
                    console.error('Error:', data.error);
                }
            } catch (error) {
                console.error('Error:', error);
            }

            setTimeout(() => {
                const chatBody = document.querySelector(".chat-body");
                chatBody.scrollTop = chatBody.scrollHeight;
            }, 100);
        }
    };

    return (
        <div>
            <button
                className={`chatbot-button ${isAnimating ? 'animating' : ''} ${isDragging ? 'dragging' : ''}`}
                onMouseDown={handleMouseDown}
                style={{ top: buttonPosition.top, left: buttonPosition.left, position: 'fixed' }}
                ref={buttonRef}
            >
                <img src="/chatbot.png" alt="Chatbot" />
            </button>

            {showChat && (
                <div className="chat-popup" ref={chatPopupRef}>
                    <div className="chat-header">
                        <button onClick={handleClose}>Close</button>
                    </div>
                    <div className="chat-body">
                        {messages.map((message, index) => (
                            <div
                                key={index}
                                className={`message-bubble ${message.sender}`}
                                dangerouslySetInnerHTML={{ __html: marked(message.text) }}
                            />
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
