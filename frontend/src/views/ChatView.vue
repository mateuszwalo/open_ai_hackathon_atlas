// filepath: c:\Users\maksk\Desktop\TheHack\open_ai_hackathon_atlas\frontend\src\views\ChatView.vue
<script setup lang="ts">
import { ref } from 'vue';
import ChatInput from '@/components/chat/ChatInput.vue';
// Import the new MessageList component
import MessageList from '@/components/chat/MessageList.vue';

// Define the message structure (can be moved to a shared types file later)
interface ChatMessage {
  id: string;
  text: string;
  sender: 'user' | 'ai';
  timestamp: Date;
  threadId?: string;
}

// Use the interface for the messages ref
const messages = ref<ChatMessage[]>([]);
const isLoading = ref(false);

function handleSendMessage(messageText: string) {
  console.log('Received message from ChatInput:', messageText);

  // Add user message using the ChatMessage interface
  messages.value.push({
    id: Date.now().toString() + '-user', // Add sender type to ID for potential key issues
    text: messageText,
    sender: 'user',
    timestamp: new Date()
  });

  isLoading.value = true;
  // Placeholder: Simulate AI response
  setTimeout(() => {
    messages.value.push({
      id: Date.now().toString() + '-ai', // Add sender type to ID
      text: 'AI response placeholder... This is a slightly longer response to test wrapping and layout.',
      sender: 'ai',
      timestamp: new Date()
    });
    isLoading.value = false;
  }, 1500);
}
</script>

<template>
  <div class="chat-view">
    <h1>Mental Health Chatbot</h1>
    <div class="chat-container">
      <!-- Replace the placeholder div with the MessageList component -->
      <MessageList :messages="messages" :is-loading="isLoading" />
      <!--
      <div class="message-list-placeholder">
        <p v-if="messages.length === 0">No messages yet. Start the conversation!</p>
        <div v-for="message in messages" :key="message.id" class="message-item">
          <strong>{{ message.sender === 'user' ? 'You' : 'AI' }}:</strong> {{ message.text }}
        </div>
        <p v-if="isLoading">AI is thinking...</p>
      </div>
      -->

      <ChatInput :disabled="isLoading" @send-message="handleSendMessage" />
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

/* Styles for the placeholder list and items are no longer needed here */
/* .message-list-placeholder { ... } */
/* .message-item { ... } */
/* .message-item strong { ... } */
/* .message-item:has(strong:contains('You')) { ... } */
/* .message-item:has(strong:contains('AI')) { ... } */
</style>