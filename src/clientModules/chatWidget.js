/**
 * Docusaurus Client Module - ChatWidget Injection
 * This module injects the ChatWidget component on every page
 */
import React from 'react';
import { createRoot } from 'react-dom/client';
import ChatWidget from '@site/src/components/ChatWidget';

let chatWidgetRoot = null;

export function onRouteDidUpdate({ location, previousLocation }) {
  // Only inject once
  if (chatWidgetRoot) {
    return;
  }

  // Create container element if it doesn't exist
  let container = document.getElementById('chat-widget-root');
  if (!container) {
    container = document.createElement('div');
    container.id = 'chat-widget-root';
    document.body.appendChild(container);
  }

  // Render the ChatWidget
  chatWidgetRoot = createRoot(container);
  chatWidgetRoot.render(<ChatWidget />);
}
