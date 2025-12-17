/**
 * TextSelectionHandler - Handles text selection and shows "Ask AI" button
 */
import React, { useState, useEffect, useCallback } from 'react';
import styles from './ChatWidget.module.css';

const MIN_SELECTION_LENGTH = 20; // Minimum characters to show button
const DEBOUNCE_DELAY = 300; // ms

export default function TextSelectionHandler({ onAskAboutSelection }) {
  const [selection, setSelection] = useState(null);
  const [buttonPosition, setButtonPosition] = useState(null);

  // Debounced selection handler
  const handleSelection = useCallback(() => {
    const sel = window.getSelection();
    const text = sel?.toString().trim();

    if (text && text.length >= MIN_SELECTION_LENGTH) {
      try {
        const range = sel.getRangeAt(0);
        const rect = range.getBoundingClientRect();

        // Position button above the selection
        setButtonPosition({
          top: rect.top + window.scrollY - 45,
          left: rect.left + rect.width / 2,
        });
        setSelection(text);
      } catch (e) {
        // Selection might be invalid
        setSelection(null);
        setButtonPosition(null);
      }
    } else {
      setSelection(null);
      setButtonPosition(null);
    }
  }, []);

  // Set up event listeners
  useEffect(() => {
    let timeoutId;

    const debouncedHandler = () => {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(handleSelection, DEBOUNCE_DELAY);
    };

    // Listen for mouse up (selection complete)
    document.addEventListener('mouseup', debouncedHandler);

    // Clear selection on scroll
    const clearSelection = () => {
      setSelection(null);
      setButtonPosition(null);
    };

    document.addEventListener('scroll', clearSelection, { passive: true });

    return () => {
      document.removeEventListener('mouseup', debouncedHandler);
      document.removeEventListener('scroll', clearSelection);
      clearTimeout(timeoutId);
    };
  }, [handleSelection]);

  // Handle button click
  const handleAskClick = () => {
    if (selection && onAskAboutSelection) {
      onAskAboutSelection(selection);
      // Clear selection after clicking
      setSelection(null);
      setButtonPosition(null);
      // Clear browser selection
      window.getSelection()?.removeAllRanges();
    }
  };

  // Don't render if no selection
  if (!selection || !buttonPosition) {
    return null;
  }

  return (
    <button
      className={styles.askAiButton}
      style={{
        top: `${buttonPosition.top}px`,
        left: `${buttonPosition.left}px`,
        transform: 'translateX(-50%)',
      }}
      onClick={handleAskClick}
    >
      <span role="img" aria-label="AI">🤖</span>
      Ask AI
    </button>
  );
}
