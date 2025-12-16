/**
 * ChatMessage component - Renders individual chat messages
 */
import React from 'react';
import styles from './ChatWidget.module.css';

export default function ChatMessage({ message }) {
  const { role, content, selected_text } = message;
  const isUser = role === 'user';

  return (
    <div className={`${styles.message} ${isUser ? styles.userMessage : styles.assistantMessage}`}>
      {/* Show selected text context for user messages */}
      {isUser && selected_text && (
        <div className={styles.selectedTextContext}>
          <span className={styles.selectedTextLabel}>Asking about:</span>
          <span className={styles.selectedTextContent}>"{selected_text}"</span>
        </div>
      )}
      <div>{content}</div>
    </div>
  );
}

/**
 * Loading indicator component
 */
export function LoadingIndicator() {
  return (
    <div className={styles.loadingIndicator}>
      <div className={styles.typingDots}>
        <span></span>
        <span></span>
        <span></span>
      </div>
    </div>
  );
}

/**
 * Welcome message component
 */
export function WelcomeMessage() {
  return (
    <div className={styles.welcomeMessage}>
      <h4>Welcome to AI Book Assistant</h4>
      <p>
        Ask me anything about the Physical AI & Humanoid Robotics textbook.
        You can also select text on any page to ask questions about specific passages.
      </p>
    </div>
  );
}

/**
 * Error message component
 */
export function ErrorMessage({ message, onRetry }) {
  return (
    <div className={styles.errorMessage}>
      <p>{message}</p>
      {onRetry && (
        <button onClick={onRetry} style={{ marginTop: '8px', cursor: 'pointer' }}>
          Try Again
        </button>
      )}
    </div>
  );
}
