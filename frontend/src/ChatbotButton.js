import React, { useState, useRef } from 'react';
import './ChatbotButton.css'; 

function ChatbotButton() {
    const [showChat, setShowChat] = useState(false);
    // Set initial position to bottom-right corner
    const [buttonPosition, setButtonPosition] = useState({ top: window.innerHeight - 120, left: window.innerWidth - 70 }); // Adjust according to the size of the button
    const buttonRef = useRef(null);

    const handleClick = () => {
        setShowChat(true);
    };

    const handleClose = () => {
        setShowChat(false);
    };

    // Dragging
    const handleMouseDown = (e) => {
        e.preventDefault(); // Prevent text selection on the webpage while dragging
        const initialX = e.clientX;
        const initialY = e.clientY;
        const initialButtonLeft = buttonPosition.left;
        const initialButtonTop = buttonPosition.top;

        const handleMouseMove = (moveEvent) => {
            const newX = initialButtonLeft + (moveEvent.clientX - initialX);
            const newY = initialButtonTop + (moveEvent.clientY - initialY);

            // Ensure the button stays within the webpage
            const pageWidth = window.innerWidth;
            const pageHeight = window.innerHeight;
            const buttonWidth = 50; 
            const buttonHeight = 50; 

            // Limit dragging to boundaries
            setButtonPosition({
                left: Math.min(Math.max(newX, 0), pageWidth - buttonWidth),
                top: Math.min(Math.max(newY, 0), pageHeight - buttonHeight),
            });
        };

        const handleMouseUp = () => {
            // Remove mousemove and mouseup listeners when the mouse button is released
            window.removeEventListener('mousemove', handleMouseMove);
            window.removeEventListener('mouseup', handleMouseUp);
        };

        window.addEventListener('mousemove', handleMouseMove);
        window.addEventListener('mouseup', handleMouseUp);
    };

    return (
        <div>
            <button
                className="chatbot-button"
                onClick={handleClick}
                onMouseDown={handleMouseDown}
                // Set position to fixed, even when users scrolls the webpage
                style={{ top: buttonPosition.top, left: buttonPosition.left, position: 'fixed' }} 
                ref={buttonRef}
            >
                <img src="/chatbot.png" alt="Chatbot" />
            </button>

            {showChat && (
                <div className="chat-popup" style={{ left: buttonPosition.left - 300, top: buttonPosition.top - 250 }}>
                    <div className="chat-header">
                        <button onClick={handleClose}>Close</button>
                    </div>
                    <div className="chat-body">
                        {/* Empty chat interface for now */}
                    </div>
                </div>
            )}
        </div>
    );
}

export default ChatbotButton;
