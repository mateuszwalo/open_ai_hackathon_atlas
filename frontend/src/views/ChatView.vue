// filepath: c:\Users\maksk\Desktop\TheHack\open_ai_hackathon_atlas\frontend\src\views\ChatView.vue
<script setup lang="ts">
import { ref } from 'vue';
// Import the new component
import ChatInput from '@/components/chat/ChatInput.vue'; // Using '@/' alias for src/

// Placeholder for future state management connection
const messages = ref<any[]>([]); // Specify type for messages array
const isLoading = ref(false); // Will track if AI is responding
// No longer need newMessage here, ChatInput manages its own state
// const newMessage = ref('');

// Renamed function parameter to avoid conflict with outer scope variable if needed
function handleSendMessage(messageText: string) {
  // Logic to send message will go here
  console.log('Received message from ChatInput:', messageText);

  // Placeholder: Add user message to list (we'll replace this with Pinia later)
  messages.value.push({ id: Date.now().toString(), text: messageText, sender: 'user', timestamp: new Date() });

  // Placeholder: Simulate AI response (we'll replace this with API call later)
  isLoading.value = true;
  setTimeout(() => {
    messages.value.push({ id: Date.now().toString(), text: 'AI response placeholder...', sender: 'ai', timestamp: new Date() });
    isLoading.value = false;
  }, 1500);
}
</script>

<template>
  <div class="chat-view">
    <h1>Mental Health Chatbot</h1>
    <div class="chat-container">
      <!-- MessageList component will go here -->
      <div class="message-list-placeholder">
        <p v-if="messages.length === 0">No messages yet. Start the conversation!</p>
        <div v-for="message in messages" :key="message.id" class="message-item">
          <strong>{{ message.sender === 'user' ? 'You' : 'AI' }}:</strong> {{ message.text }}
        </div>
        <p v-if="isLoading">AI is thinking...</p>
      </div>

      <!-- Replace the placeholder div with the ChatInput component -->
      <ChatInput :disabled="isLoading" @send-message="handleSendMessage" />
      <!--
      <div class="chat-input-placeholder">
        <input
          type="text"
          v-model="newMessage"
          placeholder="Type your message..."
          @keyup.enter="sendMessage"
          :disabled="isLoading"
        />
        <button @click="sendMessage" :disabled="isLoading || !newMessage.trim()">
          Send
        </button>
      </div>
      -->
    </div>
  </div>
</template>

<style scoped>
.chat-view {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 2rem); /* Full height minus App.vue padding */
  max-width: 800px; /* Limit width for better readability */
  margin: 0 auto; /* Center the chat view */
  font-family: 'Switzer', sans-serif; /* Use Switzer font */
}

h1 {
  font-family: 'Nohemi', sans-serif; /* Use Nohemi font for heading */
  font-weight: 600;
  color: #3c8a38; /* Primary green */
  text-align: center;
  margin-bottom: 1rem;
}

.chat-container {
  flex-grow: 1; /* Takes remaining vertical space */
  display: flex;
  flex-direction: column;
  border: 1px solid #a2e59f; /* Light green border */
  border-radius: 8px; /* Rounded corners */
  background-color: #ffffff; /* White background for chat area */
  overflow: hidden; /* Keep content within rounded corners */
}

.message-list-placeholder {
  flex-grow: 1;
  padding: 1rem;
  overflow-y: auto; /* Allow scrolling for messages */
  /* Removed border-bottom, ChatInput now provides the top border */
}

.message-item {
  margin-bottom: 0.5rem;
  padding: 0.5rem 0.75rem;
  border-radius: 8px;
  max-width: 80%;
}

.message-item strong {
  font-weight: 600; /* Slightly bolder sender name */
}

/* Basic differentiation for user/ai messages (will be refined in ChatMessage.vue) */
.message-item:has(strong:contains('You')) {
  background-color: #e8f5e9; /* Lighter green for user */
  margin-left: auto; /* Align user messages to the right */
  text-align: right;
}

.message-item:has(strong:contains('AI')) {
  background-color: #f1f8e9; /* Lighter ivory/green for AI */
  margin-right: auto; /* Align AI messages to the left */
  text-align: left;
}

/* Styles for the placeholder input are no longer needed here */
/* .chat-input-placeholder { ... } */
/* .chat-input-placeholder input { ... } */
/* .chat-input-placeholder input:disabled { ... } */
/* .chat-input-placeholder button { ... } */
/* .chat-input-placeholder button:hover { ... } */
/* .chat-input-placeholder button:disabled { ... } */
</style>