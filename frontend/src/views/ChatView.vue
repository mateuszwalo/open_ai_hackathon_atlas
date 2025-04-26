// filepath: c:\Users\maksk\Desktop\TheHack\open_ai_hackathon_atlas\frontend\src\views\ChatView.vue
<script setup lang="ts">
import ChatInput from '@/components/chat/ChatInput.vue';
import MessageList from '@/components/chat/MessageList.vue';
import { useChatStore } from '@/stores/chatStore'; // Import the chat store
import { useAuthStore } from '@/stores/authStore'; // Import auth store for logout

// Get instances of the stores
const chatStore = useChatStore();
const authStore = useAuthStore(); // Get auth store instance

// The handleSendMessage function now just calls the store action
function handleSendMessage(messageText: string) {
  console.log('Sending message via store:', messageText);
  chatStore.sendMessage(messageText); // Call the action in the chat store
}

// Function to handle logout
function handleLogout() {
  authStore.logout(); // Call the logout action from the auth store
  // The auth store's logout action should ideally call chatStore.clearChat()
}

function handleNewConversation() {
  chatStore.startNewConversation();
}
</script>

<template>
  <div class="chat-view">
    <header class="chat-header">
      <h1>Mental Health Chatbot</h1>
      <div>
        <button @click="handleNewConversation" class="new-convo-button">New Conversation</button>
        <button @click="handleLogout" class="logout-button">Logout</button>
      </div>
    </header>
    <div class="chat-container">
      <!-- Pass messages and isLoading directly from the store -->
      <MessageList :messages="chatStore.messages" :is-loading="chatStore.isLoading" />
      <!-- Display chat error if it exists -->
      <div v-if="chatStore.chatError" class="chat-error-message">
        {{ chatStore.chatError }}
      </div>
      <!-- Pass isLoading from the store to disable the input -->
      <ChatInput :disabled="chatStore.isLoading" @send-message="handleSendMessage" />
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

/* Style the header */
.chat-header {
  display: flex;
  justify-content: space-between; /* Space out title and button */
  align-items: center; /* Vertically align items */
  margin-bottom: 1rem;
}

h1 {
  font-family: 'Nohemi', sans-serif; /* Use Nohemi font for heading */
  font-weight: 600;
  color: #3c8a38; /* Primary green */
  text-align: center;
  margin: 0; /* Remove default margin */
  flex-grow: 1; /* Allow title to take space */
  padding-left: 60px; /* Add padding to center title roughly, adjust as needed */
}

.logout-button {
  padding: 0.4rem 0.8rem;
  background-color: #e57373; /* A reddish color for logout */
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-family: 'Nohemi', sans-serif;
  font-weight: 500;
  font-size: 0.9rem;
  transition: background-color 0.2s ease;
  white-space: nowrap; /* Prevent button text wrapping */
}

.logout-button:hover {
  background-color: #d32f2f; /* Darker red on hover */
}

.new-convo-button {
  margin-right: 0.5rem;
  background-color: #a2e59f;
  color: #212121;
  border: none;
  border-radius: 8px;
  padding: 0.4rem 0.8rem;
  font-family: 'Nohemi', sans-serif;
  font-weight: 500;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background-color 0.2s;
}
.new-convo-button:hover {
  background-color: #3c8a38;
  color: #fff;
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

/* Style for chat error messages */
.chat-error-message {
  color: #d32f2f; /* Red color for errors */
  background-color: #ffebee; /* Light red background */
  border-top: 1px solid #ef9a9a; /* Lighter red border */
  padding: 0.75rem;
  text-align: center;
  font-size: 0.9rem;
  font-family: 'Switzer', sans-serif;
}
</style>