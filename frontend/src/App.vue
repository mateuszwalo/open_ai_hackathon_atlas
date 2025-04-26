<script setup lang="ts">
import { RouterView } from 'vue-router'
import Sidebar from '@/components/layout/Sidebar.vue'; // Import the Sidebar
import { useAuthStore } from './stores/authStore'; // Import auth store
import { useQuestionnaireStore } from './stores/questionnaireStore'; // Import questionnaire store

const authStore = useAuthStore(); // Get auth store instance
const questionnaireStore = useQuestionnaireStore(); // Get questionnaire store instance
</script>

<template>
  <div id="app-container">
    <!-- Conditionally render Sidebar only if logged in AND questionnaire is completed -->
    <Sidebar v-if="authStore.isLoggedIn && questionnaireStore.isCompleted" />
    <main class="main-content">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
#app-container {
  display: flex; /* Use flexbox for layout */
  min-height: 100vh;
  background-color: #f8fbef; /* light ivory */
  color: #212121; /* dark gray */
  /* Remove padding from here if you want sidebar flush against edge */
  /* padding: 1rem; */
  box-sizing: border-box;
}

.main-content {
  flex-grow: 1; /* Allow main content to take remaining space */
  /* Add padding here if removed from #app-container */
  padding: 1rem;
  overflow-y: auto; /* Allow main content to scroll if needed */
  height: 100vh; /* Ensure it can scroll independently */
  box-sizing: border-box;
}

/* Adjust ChatView padding if needed, as it's now inside .main-content */
/* Example: You might need to adjust styles in ChatView.vue */
/* .chat-view { height: 100%; max-width: none; margin: 0; } */

</style>