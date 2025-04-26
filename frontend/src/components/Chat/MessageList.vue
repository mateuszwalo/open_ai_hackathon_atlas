// filepath: c:\Users\maksk\Desktop\TheHack\open_ai_hackathon_atlas\frontend\src\components\chat\MessageList.vue
<script setup lang="ts">
import { ref, watch, nextTick } from 'vue';

// Define the structure of a single message object
// This should match the structure used in ChatView and eventually Pinia
interface ChatMessage {
  id: string;
  text: string;
  sender: 'user' | 'ai';
  timestamp: Date;
  threadId?: string; // Optional thread ID
}

// Define the props this component expects from its parent (ChatView)
const props = defineProps<{
  messages: ChatMessage[]; // An array of message objects
  isLoading: boolean;      // Whether the AI is currently responding
}>();

// Create a reference to the scrollable message container element in the template
const messageContainer = ref<HTMLElement | null>(null);

// Function to scroll the container to the bottom
const scrollToBottom = () => {
  // nextTick waits for the DOM to update after new messages are added
  nextTick(() => {
    const container = messageContainer.value;
    if (container) {
      container.scrollTop = container.scrollHeight; // Set scroll position to the very bottom
    }
  });
};

// Watch for changes in the 'messages' prop array
// When the array changes (a new message is added), call scrollToBottom
watch(() => props.messages, scrollToBottom, { deep: true }); // 'deep: true' ensures watch triggers even if nested properties change (though less relevant for array additions)

// Also scroll to bottom when the component is first loaded
watch(messageContainer, (newVal) => {
  if (newVal) {
    scrollToBottom();
  }
}, { immediate: true }); // 'immediate: true' runs the watcher once initially

</script>

<template>
  <div class="message-list" ref="messageContainer">
    <p v-if="messages.length === 0" class="empty-message">
      No messages yet. Start the conversation!
    </p>
    <!-- We will replace this div with the ChatMessage component in the next step -->
    <div
      v-for="message in messages"
      :key="message.id"
      class="message-item-placeholder"
      :class="{ 'user-message': message.sender === 'user', 'ai-message': message.sender === 'ai' }"
    >
      <div class="message-content">
        {{ message.text }}
      </div>
      <!-- Basic timestamp - can be formatted better later -->
      <span class="timestamp">{{ message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }}</span>
    </div>
    <p v-if="isLoading" class="loading-indicator">
      AI is thinking...
    </p>
  </div>
</template>

<style scoped>
.message-list {
  flex-grow: 1; /* Takes up available vertical space */
  padding: 1rem;
  overflow-y: auto; /* Enables vertical scrolling */
  display: flex;
  flex-direction: column; /* Stack messages vertically */
  gap: 0.75rem; /* Space between messages */
}

.empty-message {
  text-align: center;
  color: #888;
  margin-top: auto;
  margin-bottom: auto; /* Center vertically if no messages */
}

/* Placeholder styles - will be mostly replaced by ChatMessage.vue styles */
.message-item-placeholder {
  padding: 0.6rem 0.9rem;
  border-radius: 8px;
  max-width: 80%;
  word-wrap: break-word; /* Ensure long words break */
  display: flex;
  flex-direction: column; /* Stack content and timestamp */
}

.message-content {
  font-family: 'Switzer', sans-serif;
  font-weight: 300;
  line-height: 1.5;
}

.timestamp {
  font-size: 0.7rem;
  color: #666;
  margin-top: 0.25rem;
  align-self: flex-end; /* Align timestamp to the bottom right */
}

.user-message {
  background-color: #e8f5e9; /* Lighter green for user */
  color: #212121;
  margin-left: auto; /* Align user messages to the right */
  align-items: flex-end; /* Align content to the right */
}
.user-message .timestamp {
  align-self: flex-end;
}

.ai-message {
  background-color: #f1f8e9; /* Lighter ivory/green for AI */
  color: #212121;
  margin-right: auto; /* Align AI messages to the left */
  align-items: flex-start; /* Align content to the left */
}
.ai-message .timestamp {
  align-self: flex-end; /* Still align timestamp to right within the bubble */
}
/* --- End Placeholder Styles --- */


.loading-indicator {
  text-align: center;
  color: #555;
  font-style: italic;
  padding: 0.5rem;
}
</style>