/**
 * ChatWidget - Main chat component
 * Provides floating chat interface with text selection support
 */
import React, { useState, useEffect, useRef, useCallback } from 'react';
import styles from './ChatWidget.module.css';
import ChatMessage, { LoadingIndicator, StreamingIndicator, WelcomeMessage, ErrorMessage } from './ChatMessage';
import TextSelectionHandler from './TextSelectionHandler';
import { createSession, sendMessage, sendMessageStreaming } from './api';

// Enable streaming by default (can be toggled for debugging)
const USE_STREAMING = true;

// Storage key for session persistence
const SESSION_STORAGE_KEY = 'ai_book_chat_session';

export default function ChatWidget() {
  // UI State
  const [isOpen, setIsOpen] = useState(false);
  const [inputValue, setInputValue] = useState('');

  // Chat State
  const [sessionId, setSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isStreaming, setIsStreaming] = useState(false);
  const [streamingContent, setStreamingContent] = useState('');
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
  }, [messages, isLoading, isStreaming, streamingContent, scrollToBottom]);

  // Initialize or restore session
  useEffect(() => {
    const initSession = async () => {
      // Try to restore session from storage
      const storedSessionId = localStorage.getItem(SESSION_STORAGE_KEY);

      if (storedSessionId) {
        setSessionId(storedSessionId);
      } else {
        // Create new session when widget first opens
        // We'll defer this until the user actually opens the chat
      }
    };

    initSession();
  }, []);

  // Create session when chat is opened for the first time
  const ensureSession = async () => {
    if (sessionId) return sessionId;

    try {
      const session = await createSession({
        source: window.location.pathname,
        user_agent: navigator.userAgent,
      });
      const newSessionId = session.id;
      setSessionId(newSessionId);
      localStorage.setItem(SESSION_STORAGE_KEY, newSessionId);
      return newSessionId;
    } catch (err) {
      console.error('Failed to create session:', err);
      setError('Could not connect to chat service. Please try again.');
      return null;
    }
  };

  // Handle sending a message
  const handleSend = async () => {
    const message = inputValue.trim();
    if (!message || isLoading || isStreaming) return;

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

    // Ensure we have a session
    const currentSessionId = await ensureSession();
    if (!currentSessionId) {
      return;
    }

    if (USE_STREAMING) {
      // Use streaming API
      setIsStreaming(true);
      setStreamingContent('');

      try {
        await sendMessageStreaming(
          currentSessionId,
          message,
          {
            onToken: (token) => {
              setStreamingContent((prev) => prev + token);
            },
            onDone: (data) => {
              // Add completed assistant message
              setMessages((prev) => [
                ...prev,
                {
                  id: data.message_id,
                  role: 'assistant',
                  content: streamingContent + '', // Capture final content
                },
              ]);
              setStreamingContent('');
              setIsStreaming(false);
            },
            onError: (err) => {
              console.error('Streaming error:', err);
              setError(err.message || 'Failed to get response. Please try again.');
              setStreamingContent('');
              setIsStreaming(false);
            },
          },
          contextText
        );

        // Handle case where stream completes without onDone being called
        // (fallback in case SSE doesn't properly signal completion)
        if (streamingContent) {
          setMessages((prev) => [
            ...prev,
            {
              id: `stream-${Date.now()}`,
              role: 'assistant',
              content: streamingContent,
            },
          ]);
          setStreamingContent('');
        }
        setIsStreaming(false);
      } catch (err) {
        console.error('Failed to stream message:', err);
        setError(err.message || 'Failed to get response. Please try again.');
        setStreamingContent('');
        setIsStreaming(false);
      }
    } else {
      // Use non-streaming API
      setIsLoading(true);

      try {
        // Send message to API
        const response = await sendMessage(currentSessionId, message, contextText);

        // Add assistant response
        const assistantMessage = {
          id: response.message_id,
          role: 'assistant',
          content: response.response,
        };
        setMessages((prev) => [...prev, assistantMessage]);
      } catch (err) {
        console.error('Failed to send message:', err);
        setError(err.message || 'Failed to get response. Please try again.');
      } finally {
        setIsLoading(false);
      }
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
    if (e.key === 'Enter' && !e.shiftKey && !isStreaming) {
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
            {messages.length === 0 && !isLoading && !isStreaming && <WelcomeMessage />}

            {messages.map((msg) => (
              <ChatMessage key={msg.id} message={msg} />
            ))}

            {/* Show streaming content as it arrives */}
            {isStreaming && streamingContent && (
              <ChatMessage
                message={{
                  id: 'streaming',
                  role: 'assistant',
                  content: streamingContent,
                }}
                isStreaming
              />
            )}

            {/* Show streaming indicator while waiting for first token */}
            {isStreaming && !streamingContent && <StreamingIndicator />}

            {isLoading && <LoadingIndicator />}

            {error && (
              <ErrorMessage
                message={error}
                onRetry={() => {
                  setError(null);
                  handleSend();
                }}
              />
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Selected text context indicator */}
          {selectedText && (
            <div
              style={{
                padding: '8px 16px',
                background: 'var(--ifm-color-emphasis-100)',
                borderTop: '1px solid var(--ifm-color-emphasis-200)',
                fontSize: '12px',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
              }}
            >
              <span>
                <strong>Context:</strong> "{selectedText.substring(0, 50)}..."
              </span>
              <button
                onClick={clearSelectedText}
                style={{
                  background: 'none',
                  border: 'none',
                  cursor: 'pointer',
                  color: 'var(--ifm-color-danger)',
                }}
              >
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
              disabled={isLoading || isStreaming}
            />
            <button
              className={styles.sendButton}
              onClick={handleSend}
              disabled={!inputValue.trim() || isLoading || isStreaming}
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
