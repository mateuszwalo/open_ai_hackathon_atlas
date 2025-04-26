// filepath: c:\Users\maksk\Desktop\TheHack\open_ai_hackathon_atlas\frontend\src\components\chat\ChatMessage.vue
<script setup lang="ts">
import { computed } from 'vue';
import { marked } from 'marked'; // Import marked

// Define the structure of the message prop
interface ChatMessageData {
  id: string;
  text: string;
  sender: 'user' | 'ai';
  timestamp: Date;
  threadId?: string;
}

// Define the props this component expects
const props = defineProps<{
  message: ChatMessageData;
}>();

// Determine CSS classes based on the sender
const messageClasses = computed(() => ({
  'message-item': true,
  'user-message': props.message.sender === 'user',
  'ai-message': props.message.sender === 'ai',
}));

// Format the timestamp for display
const formattedTimestamp = computed(() => {
  return props.message.timestamp.toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit',
  });
});

// New: Render markdown text to HTML
const renderedMarkdown = computed(() => {
  // Use marked.parse() to convert markdown string to HTML
  // Note: Be cautious with v-html if the source isn't fully trusted.
  // For AI responses you control, it's generally okay, but sanitize if needed.
  return marked.parse(props.message.text);
});

</script>

<template>
  <div :class="messageClasses">
    <!-- Use v-html to render the parsed markdown -->
    <div class="message-content" v-html="renderedMarkdown"></div>
    <span class="timestamp">{{ formattedTimestamp }}</span>
  </div>
</template>

<style scoped>
.message-item {
  padding: 0.6rem 0.9rem;
  border-radius: 8px; /* Rounded corners */
  max-width: 80%; /* Limit width */
  word-wrap: break-word; /* Break long words */
  display: flex;
  flex-direction: column; /* Stack content and timestamp */
  position: relative; /* Needed for potential future elements like avatars */
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05); /* Subtle shadow */
}

.message-content {
  font-family: 'Switzer', sans-serif; /* Use Switzer font */
  font-weight: 300; /* Light weight */
  line-height: 1.5; /* Improve readability */
  white-space: pre-wrap; /* Preserve line breaks from the text */
}

/* Add basic styling for common markdown elements within message-content */
.message-content :deep(p) {
  margin-bottom: 0.5em; /* Add space between paragraphs */
}
.message-content :deep(p):last-child {
  margin-bottom: -1.75rem; /* No space after the last paragraph */
}
.message-content :deep(ul),
.message-content :deep(ol) {
  padding-left: 1.5em; /* Indent lists */
  margin-bottom: 0.5em;
}
.message-content :deep(li) {
  margin-bottom: 0.25em; /* Space between list items */
}
.message-content :deep(code) {
  background-color: rgba(0, 0, 0, 0.05); /* Subtle background for inline code */
  padding: 0.2em 0.4em;
  border-radius: 4px;
  font-size: 0.9em;
  font-family: monospace;
}
.message-content :deep(pre) {
  background-color: rgba(0, 0, 0, 0.07); /* Slightly darker for code blocks */
  padding: 0.75em;
  border-radius: 4px;
  overflow-x: auto; /* Allow horizontal scrolling for long code lines */
  margin-bottom: 0.5em;
}
.message-content :deep(pre code) {
  background-color: transparent; /* Remove double background */
  padding: 0;
  font-size: 0.85em;
}
.message-content :deep(blockquote) {
  border-left: 3px solid #a2e59f; /* Use accent color for blockquote border */
  padding-left: 1em;
  margin-left: 0;
  margin-right: 0;
  margin-bottom: 0.5em;
  color: #555; /* Slightly muted text */
  font-style: italic;
}
.message-content :deep(strong) {
  font-weight: 600; /* Make bold text stand out more */
}
.message-content :deep(em) {
  font-style: italic;
}

.timestamp {
  font-size: 0.7rem;
  color: #666; /* Medium gray */
  margin-top: 0.25rem;
  align-self: flex-end; /* Align timestamp to the bottom right */
}

/* Styles for User messages */
.user-message {
  background-color: #e8f5e9; /* Lighter green */
  color: #212121; /* Dark gray text */
  margin-left: auto; /* Align to the right */
  align-items: flex-end; /* Align content to the right */
}
.user-message .timestamp {
  align-self: flex-end;
}

/* Styles for AI messages */
.ai-message {
  background-color: #f1f8e9; /* Lighter ivory/green */
  color: #212121; /* Dark gray text */
  margin-right: auto; /* Align to the left */
  align-items: flex-start; /* Align content to the left */
}
.ai-message .timestamp {
  align-self: flex-end; /* Still align timestamp to right within the bubble */
}
</style>