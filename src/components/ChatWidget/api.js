/**
 * API client for the RAG Chatbot backend
 * Simplified version matching the backend API
 */

// Default API URL - use HuggingFace Space
const DEFAULT_API_URL = 'https://habibullahio-ai-native-book-api.hf.space';

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
 * Send a chat message and get response
 * @param {string} message - User's message
 * @param {string|null} selectedText - Optional selected text context
 * @returns {Promise<Object>} Response with id, response, sources, timestamp
 */
export async function sendMessage(message, selectedText = null) {
  const body = {
    message,
  };

  if (selectedText) {
    body.selected_text = selectedText;
  }

  const apiUrl = getUrl();
  console.log('Sending message to:', `${apiUrl}/api/chat`);

  try {
    const response = await fetch(`${apiUrl}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || error.error || 'Failed to send message');
    }

    return response.json();
  } catch (err) {
    console.error('API Error:', err);
    if (err.message === 'Failed to fetch') {
      throw new Error('Cannot connect to chat server. Please check your internet connection.');
    }
    throw err;
  }
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
