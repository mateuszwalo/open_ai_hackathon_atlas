<script setup lang="ts">
import ChatInput from '@/components/chat/ChatInput.vue';
import MessageList from '@/components/chat/MessageList.vue';
import { useChatStore } from '@/stores/chatStore';
import { useAuthStore } from '@/stores/authStore';
import { ref, onMounted } from 'vue';
import axios from 'axios';

// Get instances of the stores
const chatStore = useChatStore();
const authStore = useAuthStore();

// Add state for personality data
const personalityData = ref(null);
const isLoadingPersonality = ref(false);

// Function to fetch personality data
const fetchPersonalityData = async () => {
  if (!authStore.userId) return;
  
  isLoadingPersonality.value = true;
  try {
    const response = await axios.get(
      `${import.meta.env.VITE_API_BASE_URL}/user-personality/${authStore.userId}`
    );
    personalityData.value = response.data;
  } catch (error) {
    console.error('Failed to fetch personality data:', error);
  } finally {
    isLoadingPersonality.value = false;
  }
};

// The handleSendMessage function now just calls the store action
function handleSendMessage(messageText: string) {
  console.log('Sending message via store:', messageText);
  chatStore.sendMessage(messageText);
}

// Function to handle logout
function handleLogout() {
  authStore.logout();
}

function handleNewConversation() {
  chatStore.startNewConversation();
}

onMounted(() => {
  fetchPersonalityData();
});
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
    
    <!-- Display personality insights if available -->
    <div v-if="personalityData" class="personality-card">
      <h3>Your Personality Profile</h3>
      <div class="trait-bars">
        <div class="trait-bar-container">
          <span class="trait-label">Extraversion</span>
          <div class="trait-bar-bg">
            <div class="trait-bar" :style="{ width: `${personalityData.extraversion * 100}%` }"></div>
          </div>
          <span class="trait-value">{{ (personalityData.extraversion * 100).toFixed(0) }}%</span>
        </div>
        <div class="trait-bar-container">
          <span class="trait-label">Agreeableness</span>
          <div class="trait-bar-bg">
            <div class="trait-bar" :style="{ width: `${personalityData.agreeableness * 100}%` }"></div>
          </div>
          <span class="trait-value">{{ (personalityData.agreeableness * 100).toFixed(0) }}%</span>
        </div>
        <div class="trait-bar-container">
          <span class="trait-label">Conscientiousness</span>
          <div class="trait-bar-bg">
            <div class="trait-bar" :style="{ width: `${personalityData.conscientiousness * 100}%` }"></div>
          </div>
          <span class="trait-value">{{ (personalityData.conscientiousness * 100).toFixed(0) }}%</span>
        </div>
        <div class="trait-bar-container">
          <span class="trait-label">Neuroticism</span>
          <div class="trait-bar-bg">
            <div class="trait-bar" :style="{ width: `${personalityData.neuroticism * 100}%` }"></div>
          </div>
          <span class="trait-value">{{ (personalityData.neuroticism * 100).toFixed(0) }}%</span>
        </div>
        <div class="trait-bar-container">
          <span class="trait-label">Openness</span>
          <div class="trait-bar-bg">
            <div class="trait-bar" :style="{ width: `${personalityData.openness * 100}%` }"></div>
          </div>
          <span class="trait-value">{{ (personalityData.openness * 100).toFixed(0) }}%</span>
        </div>
      </div>
    </div>
    
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
/* Add these new styles */
.personality-card {
  margin-bottom: 1rem;
  padding: 1rem;
  background-color: #f1f8e9;
  border-radius: 8px;
  border: 1px solid #a2e59f;
}

.personality-card h3 {
  color: #3c8a38;
  margin-top: 0;
  margin-bottom: 1rem;
  font-family: 'Nohemi', sans-serif;
}

.trait-bars {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.trait-bar-container {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.trait-label {
  width: 130px;
  text-align: right;
  font-size: 0.9rem;
}

.trait-bar-bg {
  flex-grow: 1;
  height: 8px;
  background-color: #e0e0e0;
  border-radius: 4px;
  overflow: hidden;
}

.trait-bar {
  height: 100%;
  background-color: #3c8a38;
}

.trait-value {
  width: 40px;
  font-size: 0.9rem;
}

/* Keep existing styles */
.chat-view {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 2rem);
  max-width: 800px;
  margin: 0 auto;
  font-family: 'Switzer', sans-serif;
}

/* Rest of your existing styles... */
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