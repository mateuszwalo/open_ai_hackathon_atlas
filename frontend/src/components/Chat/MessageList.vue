// filepath: c:\Users\maksk\Desktop\TheHack\open_ai_hackathon_atlas\frontend\src\components\chat\MessageList.vue
<script setup lang="ts">
import { ref, watch, nextTick } from 'vue';
import welcomeImage from '@/assets/images/welcome.webp'; // Import the image
import ChatMessageComponent from './ChatMessage.vue'; // Import the ChatMessage component

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
    <!-- Container for empty chat content -->
    <div v-if="messages.length === 0" class="empty-chat-content">
      <div class="welcome-image-container">
        <img :src="welcomeImage" alt="Welcome illustration" class="welcome-image" />
      </div>
      <p class="empty-message">
        Hi Max, how can I help you?
      </p>
    </div>

    <!-- Use the actual ChatMessage component here -->
    <ChatMessageComponent
      v-for="message in messages"
      :key="message.id"
      :message="message"
    />
    <!-- The old placeholder div below should be removed -->
    <!--
    <div
      v-for="message in messages"
      :key="message.id"
      class="message-item-placeholder"
      :class="{ 'user-message': message.sender === 'user', 'ai-message': message.sender === 'ai' }"
    >
      <div class="message-content">
        {{ message.text }}
      </div>
      <span class="timestamp">{{ message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }}</span>
    </div>
    -->

    <p v-if="isLoading" class="loading-indicator">
      AI is thinking
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

/* New container for empty state */
.empty-chat-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: #888;
  margin-top: auto;
  margin-bottom: auto; /* Center vertically */
}

/* Container to clip the image */
.welcome-image-container {
  width: 30%;
  max-width: 200px; /* Adjust max-width as needed */
  height: 240px; /* Adjust height to control how much of the top is shown */
  overflow: hidden; /* Clip the image */
  margin-bottom: 1rem; /* Space between image and text */
  border-radius: 70px; /* Optional: round corners */
}

.welcome-image {
  display: block;
  width: 100%;
  height: auto; /* Maintain aspect ratio */
  object-fit: cover; /* Cover the container */
  object-position: top center; /* Show the top part */
}

.empty-message {
  margin-top: 0;
  margin-bottom: 0;
}

/* --- Remove Placeholder Styles --- */
/* Remove .message-item-placeholder, .message-content, .timestamp, .user-message, .ai-message rules */
/* These styles are now handled within ChatMessage.vue */
/* --- End Remove Placeholder Styles --- */


/* Keep loading indicator styles */
.loading-indicator {
  text-align: center;
  color: #555;
  font-style: italic;
  padding: 0.5rem;
}
.loading-indicator::after {
  content: '.';
  animation: thinking-ellipsis-dots 1.5s infinite steps(1, end);
  display: inline-block;
  vertical-align: bottom;
  overflow: hidden;
  width: 1.2em;
  text-align: left;
}

@keyframes thinking-ellipsis-dots {
  0% { content: '.'; }
  33% { content: '..'; }
  66% { content: '...'; }
  100% { content: '.'; }
}

</style>