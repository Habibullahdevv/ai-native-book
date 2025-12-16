/**
 * API client for the RAG Chatbot backend
 */

// API base URL - defaults to localhost for development
const API_BASE_URL = typeof window !== 'undefined'
  ? (window.__CHAT_API_URL__ || 'http://localhost:8000')
  : 'http://localhost:8000';

/**
 * Create a new chat session
 * @param {Object} metadata - Optional session metadata
 * @returns {Promise<Object>} Session object with id
 */
export async function createSession(metadata = {}) {
  const response = await fetch(`${API_BASE_URL}/api/sessions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ metadata }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.error || 'Failed to create session');
  }

  return response.json();
}

/**
 * Get session with messages
 * @param {string} sessionId - Session UUID
 * @returns {Promise<Object>} Session with messages array
 */
export async function getSession(sessionId) {
  const response = await fetch(`${API_BASE_URL}/api/sessions/${sessionId}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    if (response.status === 404) {
      return null;
    }
    const error = await response.json().catch(() => ({}));
    throw new Error(error.error || 'Failed to get session');
  }

  return response.json();
}

/**
 * Send a chat message and get response
 * @param {string} sessionId - Session UUID
 * @param {string} message - User's message
 * @param {string|null} selectedText - Optional selected text context
 * @returns {Promise<Object>} Response with message_id and response text
 */
export async function sendMessage(sessionId, message, selectedText = null) {
  const body = {
    session_id: sessionId,
    message,
  };

  if (selectedText) {
    body.selected_text = selectedText;
  }

  const response = await fetch(`${API_BASE_URL}/api/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.error || 'Failed to send message');
  }

  return response.json();
}

/**
 * Check API health
 * @returns {Promise<Object>} Health status
 */
export async function checkHealth() {
  const response = await fetch(`${API_BASE_URL}/api/health`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error('API health check failed');
  }

  return response.json();
}

/**
 * Set custom API URL (for configuration)
 * @param {string} url - API base URL
 */
export function setApiUrl(url) {
  if (typeof window !== 'undefined') {
    window.__CHAT_API_URL__ = url;
  }
}
