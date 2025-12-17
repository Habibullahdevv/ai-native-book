# AI Native Book

A comprehensive guide to Physical AI and Humanoid Robotics, built with Docusaurus and featuring an AI-powered chatbot assistant.

## Architecture Overview

```
+---------------------------+         +---------------------------+
|    Docusaurus Frontend    |         |      FastAPI Backend      |
|    (GitHub Pages)         |         |    (HuggingFace Spaces)   |
+---------------------------+         +---------------------------+
|                           |         |                           |
|  +--------------------+   |  HTTP   |  +--------------------+   |
|  |   ChatWidget.js    |<----------->|  |   /api/chat        |   |
|  +--------------------+   |  SSE    |  +--------------------+   |
|          |                |         |          |                |
|  +--------------------+   |         |  +--------------------+   |
|  | TextSelection      |   |         |  |   Google Gemini    |   |
|  | Handler.js         |   |         |  |   (LLM)            |   |
|  +--------------------+   |         |  +--------------------+   |
|                           |         |                           |
+---------------------------+         +---------------------------+
```

## How the Chatbot Works

### Frontend Components

The chatbot is implemented as a floating widget that appears on every page:

1. **ChatWidget.js** - Main chat component
   - Floating button (bottom-right corner)
   - Expandable chat panel with message history
   - Session persistence via localStorage
   - Streaming response support (SSE)

2. **TextSelectionHandler.js** - Text selection feature
   - Detects when user selects text (20+ characters)
   - Shows "Ask AI" button above selection
   - Passes selected text as context to the chat

3. **api.js** - API client
   - Creates chat sessions
   - Sends messages (with optional selected text context)
   - Handles streaming responses via Server-Sent Events

4. **ChatMessage.js** - Message rendering
   - User and assistant message bubbles
   - Loading and streaming indicators
   - Error handling with retry

### Layout Injection

The chatbot is injected via Docusaurus client module (`src/clientModules/chatWidget.js`):

```javascript
// Injects ChatWidget on every page load
export function onRouteDidUpdate() {
  // Creates a container div and renders ChatWidget
}
```

## Selected-Text Mode

When a user selects text on any page:

1. **Selection Detection**: `TextSelectionHandler` monitors `mouseup` events
2. **Threshold Check**: Only shows button if selection >= 20 characters
3. **Button Display**: "Ask AI" button appears above the selection
4. **Context Passing**: Clicking sends selected text as context with the next question
5. **Visual Indicator**: Chat input shows "Ask about the selected text..."

### API Flow

```
User selects text -> Click "Ask AI" -> Chat opens with context
-> User types question -> API receives: { message, selected_text }
-> LLM uses both to generate contextual response
```

## Configuration

### Chat API URL

Set via environment variable at build time:

```bash
CHAT_API_URL="https://your-api-url.com" npm run build
```

Or in `docusaurus.config.js`:

```javascript
customFields: {
  chatApiUrl: process.env.CHAT_API_URL || 'http://localhost:8000',
}
```

## Development

### Prerequisites

- Node.js >= 20.0.0
- npm

### Local Development

```bash
# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build

# Serve production build locally
npm run serve
```

### Backend

The backend API is deployed separately on HuggingFace Spaces. See `backend/` directory for the FastAPI implementation.

## Deployment

- **Frontend**: GitHub Pages (via `npm run deploy`)
- **Backend**: HuggingFace Spaces

## Project Structure

```
ai-native-book/
├── docs/                    # Book content (Markdown)
├── src/
│   ├── components/
│   │   └── ChatWidget/      # Chatbot components
│   │       ├── ChatWidget.js
│   │       ├── ChatWidget.module.css
│   │       ├── ChatMessage.js
│   │       ├── TextSelectionHandler.js
│   │       └── api.js
│   ├── clientModules/
│   │   └── chatWidget.js    # Docusaurus client module
│   ├── css/
│   │   └── custom.css
│   └── pages/
├── backend/                 # FastAPI backend (separate deployment)
├── static/                  # Static assets
├── docusaurus.config.js     # Docusaurus configuration
└── package.json
```

## License

MIT
