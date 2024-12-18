import React, { useState, useRef, useEffect } from "react";
import { marked } from "marked";
import "./ChatbotButton.css";

function ChatbotButton({ isSampleMode }) {
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
  const [fontSize, setFontSize] = useState(14);
  const [showInitialMessage, setShowInitialMessage] = useState(true); // Controls the initial message
  const [showDragMessage, setShowDragMessage] = useState(false); // New state for drag message

  const buttonRef = useRef(null);
  const chatPopupRef = useRef(null);

  const popupWidth = 300;
  const popupHeight = 500;
  const buttonWidth = 60;
  const buttonHeight = 60;
  const margin = 10; // Margin from the edges of the screen

  const increaseFontSize = () => {
    if (fontSize < 20) {
      setFontSize((prevSize) => prevSize + 2);
    }
  };

  const decreaseFontSize = () => {
    if (fontSize > 10) {
      setFontSize((prevSize) => prevSize - 2);
    }
  };

  const calculateChatPosition = () => {
    if (!chatMode) return null;

    if (chatMode === "topleft") {
      return {
        left: buttonPosition.left - popupWidth,
        top: buttonPosition.top - popupHeight,
      };
    } else {
      return {
        left: buttonPosition.left + buttonWidth + margin,
        top: buttonPosition.top + buttonHeight + margin,
      };
    }
  };

  const determineChatMode = () => {
    const hasSpaceLeft = buttonPosition.left > popupWidth + margin;
    const hasSpaceTop = buttonPosition.top > popupHeight + margin;

    return hasSpaceLeft && hasSpaceTop ? "topleft" : "bottomright";
  };

  const toggleChat = () => {
    setShowInitialMessage(false); // Hide initial message when toggling chat

    if (showChat) {
      setIsAnimating(true);
      setShowChat(false);
      setChatMode(null);

      // Animate back to original position
      const animateBackToStart = () => {
        if (buttonRef.current) {
          buttonRef.current.classList.add("animating");
        }
        setButtonPosition(startPosition);
        setTimeout(() => {
          setIsAnimating(false);
          if (buttonRef.current) {
            buttonRef.current.classList.remove("animating");
          }
        }, 300);
      };
      requestAnimationFrame(animateBackToStart);
    } else {
      const mode = determineChatMode();
      setChatMode(mode);
      setShowChat(true);

      if (messages.length === 0) {
        setMessages([
          {
            text: "Hi there! I'm SmartChart, feel free to ask me anything!",
            sender: "bot",
          },
        ]);
      }

      // Show the "You can drag me anywhere" message
      setShowDragMessage(true);

      // Hide the drag message after 5 seconds
      setTimeout(() => {
        setShowDragMessage(false);
      }, 5000); // Adjust the duration as needed
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
        setShowDragMessage(false); // Hide the drag message when dragging starts
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
          if (chatMode === "topleft") {
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

      try {
        const headers = {
          "Content-Type": "application/json",
        };

        if (!isSampleMode && localStorage.getItem("authToken")) {
          headers["Authorization"] = `Bearer ${localStorage.getItem(
            "authToken"
          )}`;
        }

        const requestBody = {
          message: newMessage,
          is_sample: Boolean(isSampleMode),
        };

        const response = await fetch("http://localhost:8000/api/chat/", {
          method: "POST",
          headers: headers,
          body: JSON.stringify(requestBody),
        });

        const data = await response.json();

        if (data.success) {
          setMessages((prevMessages) => [
            ...prevMessages,
            { text: data.message, sender: "bot" },
          ]);
        } else {
          console.error("Error:", data.error);
          setMessages((prevMessages) => [
            ...prevMessages,
            {
              text: "Sorry, I encountered an error. Please try again.",
              sender: "bot",
            },
          ]);
        }
      } catch (error) {
        console.error("Error:", error);
        setMessages((prevMessages) => [
          ...prevMessages,
          {
            text: "Sorry, I'm having trouble connecting to the server. Please check your internet connection and try again.",
            sender: "bot",
          },
        ]);
      }

      setTimeout(() => {
        const chatBody = document.querySelector(".chat-body");
        if (chatBody) {
          chatBody.scrollTop = chatBody.scrollHeight;
        }
      }, 100);
    }
  };

  const chatPosition = calculateChatPosition();

  return (
    <div>
      <div
        className="chatbot-container"
        style={{
          top: buttonPosition.top,
          left: buttonPosition.left,
          position: "fixed",
          transition: isAnimating ? "all 0.3s ease-in-out" : "none",
        }}
        onMouseDown={handleMouseDown}
      >
        <button
          className={`chatbot-button ${isAnimating ? "animating" : ""} ${
            isDragging ? "dragging" : ""
          }`}
          ref={buttonRef}
        >
          <img src="/chatbot.png" alt="Chatbot" />
        </button>
        {showInitialMessage && (
          <div className="chatbot-initial-message">Hi - ask me anything!</div>
        )}
        {!showInitialMessage && showDragMessage && (
          <div className="chatbot-drag-message">You can drag me anywhere!</div>
        )}
      </div>

      {showChat && chatPosition && (
        <div
          className="chat-popup"
          ref={chatPopupRef}
          style={{
            position: "fixed",
            top: chatPosition.top,
            left: chatPosition.left,
            transition: isDragging ? "none" : "all 0.3s ease",
          }}
        >
          <div className="chat-header">
            <div className="font-controls">
              <button onClick={decreaseFontSize} className="font-button">
                A-
              </button>
              <span className="font-size-display">{fontSize}px</span>
              <button onClick={increaseFontSize} className="font-button">
                A+
              </button>
            </div>
            <button onClick={handleClose}>Close</button>
          </div>
          <div className="chat-body">
            {messages.map((message, index) => (
              <div
                key={index}
                className={`message-bubble ${message.sender}`}
                style={{ fontSize: `${fontSize}px` }}
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

ChatbotButton.defaultProps = {
  isSampleMode: false,
};

export default ChatbotButton;
