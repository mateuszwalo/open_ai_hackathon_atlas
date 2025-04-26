// filepath: c:\Users\maksk\Desktop\TheHack\open_ai_hackathon_atlas\frontend\src\components\chat\ChatMessage.vue
<script setup lang="ts">
import { computed } from 'vue';

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
</script>

<template>
  <div :class="messageClasses">
    <div class="message-content">
      {{ message.text }}
    </div>
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