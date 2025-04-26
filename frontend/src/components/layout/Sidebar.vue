<script setup lang="ts">
import { ref } from 'vue';
import { useChatStore } from '@/stores/chatStore';
import { useAuthStore } from '@/stores/authStore';
import { useRouter } from 'vue-router';

const chatStore = useChatStore();
const authStore = useAuthStore();
const router = useRouter();

// Placeholder for previous chat threads - you'll need to implement
// fetching and managing multiple threads later.
const previousChats = ref([
  { id: 'thread-1', name: 'Heartbrake on monday' },
  { id: 'thread-2', name: 'Misunderstanding with Dave' },
  { id: 'thread-3', name: 'Good day turned bad' },
  { id: 'thread-4', name: 'Introduction' },
]);

function selectChat(threadId: string) {
  // Placeholder: Implement logic to load a specific chat thread
  console.log('Load chat:', threadId);
  // Example: chatStore.loadConversation(threadId);
  // Navigate back to chat view if selecting a chat
  router.push('/');
}

function startNewChat() {
  chatStore.startNewConversation();
  // Optionally navigate if needed, though ChatView might handle the display update
  router.push('/');
}

function goToJournal() {
  router.push('/journal');
}

function goToAccount() {
  // Placeholder: Navigate to an account page when created
  console.log('Navigate to Account');
  // router.push('/account');
}

function goToSettings() {
  // Placeholder: Navigate to a settings page when created
  console.log('Navigate to Settings');
  // router.push('/settings');
}

function handleLogout() {
  authStore.logout();
}
</script>

<template>
  <aside class="sidebar">
    <button @click="goToJournal" class="journal-button">
      📅 Daily Journal
    </button>
    <button @click="startNewChat" class="new-chat-button">
      + New Chat
    </button>

    <nav class="chat-history">
      <h2>History</h2>
      <ul>
        <li
          v-for="chat in previousChats"
          :key="chat.id"
          @click="selectChat(chat.id)"
          :class="{ active: chat.id === chatStore.currentThreadId }"
        >
          {{ chat.name }}
        </li>
        <!-- Add more chat history items here -->
      </ul>
    </nav>

    <div class="sidebar-footer">
      <button @click="goToAccount" class="icon-button account-button">
        👤 Account
      </button>
      <button @click="goToSettings" class="icon-button settings-button">
        ⚙️ Settings
      </button>
       <button @click="handleLogout" class="icon-button logout-button">
        🚪 Logout
      </button>
    </div>
  </aside>
</template>

<style scoped>
.sidebar {
  width: 260px;
  background-color: #e8f5e9; /* Lighter green */
  border-right: 1px solid #a2e59f; /* Light green border */
  display: flex;
  flex-direction: column;
  height: 100vh; /* Full viewport height */
  color: #212121; /* Dark gray text */
  font-family: 'Switzer', sans-serif;
}

.journal-button, /* Add journal button to shared styles */
.new-chat-button {
  border: none;
  border-radius: 8px;
  padding: 0.75rem 1rem;
  margin: 0.5rem 1rem 0.5rem 1rem; /* Adjust margin */
  font-family: 'Nohemi', sans-serif;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
  text-align: center; /* Center text */
}

.journal-button {
  background-color: #a2e59f; /* Accent light green */
  color: #212121; /* Dark text */
  margin-top: 1rem; /* Add margin top */
}
.journal-button:hover {
  background-color: #8bc34a; /* Slightly darker accent green */
}

.new-chat-button {
  background-color: #3c8a38; /* Primary green */
  color: white;
  /* margin-top: 0.5rem; Remove top margin if journal button is above */
}
.new-chat-button:hover {
  background-color: #2e6b2c; /* Darker green */
}

.chat-history {
  flex-grow: 1; /* Takes available space */
  overflow-y: auto;
  padding: 0 1rem;
  margin-top: 1rem; /* Add space above history */
}
.chat-history h2 {
  font-family: 'Nohemi', sans-serif;
  font-size: 0.9rem;
  color: #555;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.5rem;
  padding-left: 0.5rem;
}
.chat-history ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.chat-history li {
  padding: 0.6rem 0.8rem;
  border-radius: 8px;
  cursor: pointer;
  margin-bottom: 0.25rem;
  font-size: 0.95rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  transition: background-color 0.2s;
}
.chat-history li:hover {
  background-color: #dcedc8; /* Slightly darker light green */
}
.chat-history li.active {
  background-color: #c5e1a5; /* Even darker */
  font-weight: 500;
}

.sidebar-footer {
  padding: 1rem;
  border-top: 1px solid #a2e59f;
  display: flex;
  flex-direction: column;
  gap: 0.5rem; /* Space between buttons */
}

.icon-button {
  background: none;
  border: none;
  color: #333;
  text-align: left;
  padding: 0.5rem 0.8rem;
  border-radius: 8px;
  cursor: pointer;
  font-family: 'Switzer', sans-serif;
  font-size: 0.95rem;
  transition: background-color 0.2s;
  display: flex;
  align-items: center;
  gap: 0.75rem; /* Space between icon and text */
}
.icon-button:hover {
  background-color: #dcedc8;
}

.logout-button {
    color: #c62828; /* Reddish color for logout */
}
.logout-button:hover {
    background-color: #ffebee; /* Light red background on hover */
}

/* Basic scrollbar styling */
.chat-history::-webkit-scrollbar {
  width: 6px;
}
.chat-history::-webkit-scrollbar-thumb {
  background-color: #a2e59f;
  border-radius: 3px;
}
.chat-history::-webkit-scrollbar-track {
  background-color: transparent;
}
</style>