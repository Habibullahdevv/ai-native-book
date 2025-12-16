/**
 * API client for the RAG Chatbot backend
 */

// Default API URL for development
const DEFAULT_API_URL = 'http://localhost:8000';

/**
 * Get the API base URL from Docusaurus config or fallback
 * @returns {string} API base URL
 */
function getApiBaseUrl() {
  // Check for runtime override first
  if (typeof window !== 'undefined' && window.__CHAT_API_URL__) {
    return window.__CHAT_API_URL__;
  }

  // Try to get from Docusaurus config (injected at build time)
  if (typeof window !== 'undefined' && window.__DOCUSAURUS__?.siteConfig?.customFields?.chatApiUrl) {
    return window.__DOCUSAURUS__.siteConfig.customFields.chatApiUrl;
  }

  return DEFAULT_API_URL;
}

// Lazy-evaluated API base URL
const getUrl = () => getApiBaseUrl();

/**
 * Create a new chat session
 * @param {Object} metadata - Optional session metadata
 * @returns {Promise<Object>} Session object with id
 */
export async function createSession(metadata = {}) {
  const response = await fetch(`${getUrl()}/api/sessions`, {
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
  const response = await fetch(`${getUrl()}/api/sessions/${sessionId}`, {
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

  const response = await fetch(`${getUrl()}/api/chat`, {
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
  const response = await fetch(`${getUrl()}/api/health`, {
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

/**
 * Send a chat message and stream the response via SSE
 * @param {string} sessionId - Session UUID
 * @param {string} message - User's message
 * @param {Object} callbacks - Callback functions for streaming events
 * @param {Function} callbacks.onToken - Called for each token received
 * @param {Function} callbacks.onDone - Called when stream completes
 * @param {Function} callbacks.onError - Called on error
 * @param {string|null} selectedText - Optional selected text context
 * @returns {Promise<void>}
 */
export async function sendMessageStreaming(
  sessionId,
  message,
  { onToken, onDone, onError },
  selectedText = null
) {
  const body = {
    session_id: sessionId,
    message,
  };

  if (selectedText) {
    body.selected_text = selectedText;
  }

  try {
    const response = await fetch(`${getUrl()}/api/chat/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || error.error || 'Failed to stream message');
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();

      if (done) {
        break;
      }

      buffer += decoder.decode(value, { stream: true });

      // Process complete SSE events (each ends with \n\n)
      const events = buffer.split('\n\n');
      buffer = events.pop() || ''; // Keep incomplete event in buffer

      for (const event of events) {
        if (!event.trim()) continue;

        // Parse SSE data line
        const dataMatch = event.match(/^data: (.+)$/m);
        if (!dataMatch) continue;

        try {
          const data = JSON.parse(dataMatch[1]);

          switch (data.type) {
            case 'token':
              if (onToken) onToken(data.content);
              break;
            case 'done':
              if (onDone) onDone(data);
              return;
            case 'error':
              if (onError) onError(new Error(data.error));
              return;
          }
        } catch (parseError) {
          console.error('Failed to parse SSE event:', parseError);
        }
      }
    }
  } catch (error) {
    if (onError) {
      onError(error);
    } else {
      throw error;
    }
  }
}
