import React, { useState, useRef, useEffect } from "react";
import { marked } from "marked";
import "./ChatbotButton.css";

function ChatbotButton() {
  const [showChat, setShowChat] = useState(false);
  const [messages, setMessages] = useState([]); // Store chat messages
  const [newMessage, setNewMessage] = useState(""); // Store input text
  const [buttonPosition, setButtonPosition] = useState({
    top: window.innerHeight - 120,
    left: window.innerWidth - 70,
  });
  const [startPosition, setStartPosition] = useState({
    top: window.innerHeight - 120,
    left: window.innerWidth - 70,
  });
  const [chatMode, setChatMode] = useState(null);
  const [isAnimating, setIsAnimating] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const buttonRef = useRef(null);
  const chatPopupRef = useRef(null);

  const popupWidth = 300;
  const popupHeight = 500;
  const buttonWidth = 60;
  const buttonHeight = 60;
  const margin = 10; // Margin from the edges of the screen

  const calculateChatPosition = () => {
    if (!chatMode) return null;

    if (chatMode === 'topleft') {
      return {
        left: buttonPosition.left - popupWidth,
        top: buttonPosition.top - popupHeight
      };
    } else {
      return {
        left: buttonPosition.left + buttonWidth + margin,
        top: buttonPosition.top + buttonHeight + margin
      };
    }
  };

  const determineChatMode = () => {
    const hasSpaceLeft = buttonPosition.left > (popupWidth + margin);
    const hasSpaceTop = buttonPosition.top > (popupHeight + margin);

    return (hasSpaceLeft && hasSpaceTop) ? 'topleft' : 'bottomright';
  };

  const toggleChat = () => {
    if (showChat) {
      setIsAnimating(true);
      setShowChat(false);
      setChatMode(null);
      setTimeout(() => {
        setButtonPosition(startPosition);
        setTimeout(() => setIsAnimating(false), 300); // Match this with the CSS transition duration
      }, 0);
    } else {
      const mode = determineChatMode();
      setChatMode(mode);
      setShowChat(true);

      // Display greeting message if no messages are present
      if (messages.length === 0) {
        setMessages([
          {
            text: "Hi there! I'm SmartChart, feel free to ask me anything!",
            sender: "bot",
          },
        ]);
      }
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

        let minLeft = margin;
        let maxLeft = pageWidth - buttonWidth - margin;
        let minTop = margin;
        let maxTop = pageHeight - buttonHeight - margin;

        if (showChat) {
          if (chatMode === 'topleft') {
            minLeft = popupWidth + margin;
            minTop = popupHeight + margin;
          } else {
            maxLeft = pageWidth - (popupWidth + buttonWidth + margin * 2);
            maxTop = pageHeight - (popupHeight + buttonHeight + margin * 2);
          }
        }

        const newButtonPosition = {
          left: Math.min(Math.max(newX, minLeft), maxLeft),
          top: Math.min(Math.max(newY, minTop), maxTop),
        };

        setButtonPosition(newButtonPosition);
      }
    };

    const handleMouseUp = () => {
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseup", handleMouseUp);
      setIsDragging(false);

      if (!hasMoved) {
        toggleChat();
      }
    };

    window.addEventListener("mousemove", handleMouseMove);
    window.addEventListener("mouseup", handleMouseUp);
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (newMessage.trim() !== "") {
      setMessages([...messages, { text: newMessage, sender: "user" }]);
      setNewMessage("");
      // Send POST request to backend
      try {
        const response = await fetch("http://localhost:8000/api/chat/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ message: newMessage }), // Send the content of the message
        });

        const data = await response.json();

        if (response.ok) {
          setMessages((prevMessages) => [
            ...prevMessages,
            { text: data.message, sender: "bot" },
          ]);
        } else {
          console.error("Error:", data.error);
        }
      } catch (error) {
        console.error("Error:", error);
      }

      setTimeout(() => {
        const chatBody = document.querySelector(".chat-body");
        chatBody.scrollTop = chatBody.scrollHeight;
      }, 100);
    }
  };

  const chatPosition = calculateChatPosition();

  return (
    <div>
      <button
        className={`chatbot-button ${isAnimating ? "animating" : ""} ${
          isDragging ? "dragging" : ""
        }`}
        onMouseDown={handleMouseDown}
        style={{
          top: buttonPosition.top,
          left: buttonPosition.left,
          position: "fixed",
        }}
        ref={buttonRef}
      >
        <img src="/chatbot.png" alt="Chatbot" />
      </button>

      {showChat && chatPosition && (
        <div 
          className="chat-popup" 
          ref={chatPopupRef}
          style={{ 
            position: "fixed",
            top: chatPosition.top,
            left: chatPosition.left,
            transition: isDragging ? "none" : "all 0.3s ease"
          }}
        >
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
              <button type="submit" className="send-button">
                Send
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default ChatbotButton;
