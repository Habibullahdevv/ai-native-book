/**
 * ChatWidget - Main chat component
 * Provides floating chat interface with text selection support
 */
import React, { useState, useEffect, useRef, useCallback } from 'react';
import styles from './ChatWidget.module.css';
import ChatMessage, { LoadingIndicator, WelcomeMessage, ErrorMessage } from './ChatMessage';
import TextSelectionHandler from './TextSelectionHandler';
import { sendMessage } from './api';

export default function ChatWidget() {
  // UI State
  const [isOpen, setIsOpen] = useState(false);
  const [inputValue, setInputValue] = useState('');

  // Chat State
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Selected text context
  const [selectedText, setSelectedText] = useState(null);

  // Ref for scrolling
  const messagesEndRef = useRef(null);

  // Scroll to bottom when messages change
  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading, scrollToBottom]);

  // Handle sending a message
  const handleSend = async () => {
    const message = inputValue.trim();
    if (!message || isLoading) return;

    // Clear input
    setInputValue('');
    setError(null);

    // Add user message to UI immediately
    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: message,
      selected_text: selectedText,
    };
    setMessages((prev) => [...prev, userMessage]);

    // Clear selected text after using it
    const contextText = selectedText;
    setSelectedText(null);

    setIsLoading(true);

    try {
      // Send message to API
      const response = await sendMessage(message, contextText);

      // Add assistant response
      const assistantMessage = {
        id: response.id || Date.now() + 1,
        role: 'assistant',
        content: response.response,
        sources: response.sources || [],
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      console.error('Failed to send message:', err);
      setError(err.message || 'Failed to get response. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  // Handle text selection from the page
  const handleAskAboutSelection = (text) => {
    setSelectedText(text);
    setIsOpen(true);
    // Focus the input
    setTimeout(() => {
      document.querySelector(`.${styles.inputField}`)?.focus();
    }, 100);
  };

  // Handle Enter key
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  // Clear selected text context
  const clearSelectedText = () => {
    setSelectedText(null);
  };

  return (
    <>
      {/* Text selection handler - always active */}
      <TextSelectionHandler onAskAboutSelection={handleAskAboutSelection} />

      {/* Floating chat button */}
      <button
        className={`${styles.chatButton} ${isOpen ? styles.open : ''}`}
        onClick={() => setIsOpen(!isOpen)}
        aria-label={isOpen ? 'Close chat' : 'Open chat'}
      >
        {isOpen ? '✕' : '💬'}
      </button>

      {/* Chat panel */}
      {isOpen && (
        <div className={styles.chatPanel}>
          {/* Header */}
          <div className={styles.chatHeader}>
            <h3>AI Book Assistant</h3>
            <button
              className={styles.closeButton}
              onClick={() => setIsOpen(false)}
              aria-label="Close chat"
            >
              ✕
            </button>
          </div>

          {/* Messages area */}
          <div className={styles.messagesContainer}>
            {messages.length === 0 && !isLoading && <WelcomeMessage />}

            {messages.map((msg) => (
              <ChatMessage key={msg.id} message={msg} />
            ))}

            {isLoading && <LoadingIndicator />}

            {error && (
              <ErrorMessage
                message={error}
                onRetry={() => {
                  setError(null);
                }}
              />
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Selected text context indicator */}
          {selectedText && (
            <div className={styles.contextIndicator}>
              <span>
                <strong>Context:</strong> "{selectedText.length > 50 ? selectedText.substring(0, 50) + '...' : selectedText}"
              </span>
              <button onClick={clearSelectedText} aria-label="Clear context">
                ✕
              </button>
            </div>
          )}

          {/* Input area */}
          <div className={styles.inputContainer}>
            <input
              type="text"
              className={styles.inputField}
              placeholder={
                selectedText
                  ? 'Ask about the selected text...'
                  : 'Ask about the book...'
              }
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleKeyDown}
              disabled={isLoading}
            />
            <button
              className={styles.sendButton}
              onClick={handleSend}
              disabled={!inputValue.trim() || isLoading}
              aria-label="Send message"
            >
              ➤
            </button>
          </div>
        </div>
      )}
    </>
  );
}
