<!-- filepath: c:\Users\maksk\Desktop\TheHack\open_ai_hackathon_atlas\frontend\src\views\LoginView.vue -->
<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '@/stores/authStore'; // Import the store we just created
import { useRouter } from 'vue-router'; // Import useRouter to navigate

const authStore = useAuthStore(); // Get an instance of the auth store
const router = useRouter(); // Get router instance

// Refs to store the username and password entered by the user
const username = ref('');
const password = ref('');

// Function called when the login form is submitted
const handleLogin = async () => {
  // Call the login action from the auth store
  await authStore.login({ username: username.value, password: password.value });
  // The store action handles redirection on success/failure
};

// Function to navigate to the registration page
const goToRegister = () => {
  router.push('/register'); // Navigate to the '/register' route
};
</script>

<template>
  <div class="auth-view">
    <h1>Login</h1>
    <!-- Form calls handleLogin when submitted -->
    <form @submit.prevent="handleLogin" class="auth-form">
      <div class="form-group">
        <label for="username">Username</label>
        <!-- v-model links the input value to the username ref -->
        <input type="text" id="username" v-model="username" required />
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <!-- v-model links the input value to the password ref -->
        <input type="password" id="password" v-model="password" required />
      </div>
      <!-- Show error message from the store if it exists -->
      <div v-if="authStore.authError" class="error-message">
        {{ authStore.authError }}
      </div>
      <!-- Disable button while loading, change text -->
      <button type="submit" :disabled="authStore.isLoading">
        {{ authStore.isLoading ? 'Logging in...' : 'Login' }}
      </button>
    </form>
    <!-- Link to switch to the registration page -->
    <p class="switch-link">
      Don't have an account? <button @click="goToRegister" class="link-button">Register here</button>
    </p>
  </div>
</template>

<style scoped>
/* Basic styling for the login form, using colors from styling.md */
.auth-view {
  max-width: 400px;
  margin: 4rem auto; /* Center the box */
  padding: 2rem;
  border: 1px solid #a2e59f; /* Light green border */
  border-radius: 8px; /* Rounded corners */
  background-color: #ffffff; /* White background */
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  font-family: 'Switzer', sans-serif; /* Use Switzer font */
}

h1 {
  font-family: 'Nohemi', sans-serif; /* Use Nohemi font */
  color: #3c8a38; /* Primary green */
  text-align: center;
  margin-bottom: 1.5rem;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1rem; /* Space between form elements */
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 0.3rem;
  font-weight: 500;
  color: #555;
}

.form-group input {
  padding: 0.6rem 0.8rem;
  border: 1px solid #ccc;
  border-radius: 8px; /* Rounded corners */
  font-family: 'Switzer', sans-serif;
  font-size: 1rem;
  transition: border-color 0.2s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #3c8a38; /* Primary green */
  box-shadow: 0 0 0 2px rgba(60, 138, 56, 0.2);
}

button[type="submit"] { /* Style only the submit button */
  padding: 0.7rem 1rem;
  background-color: #3c8a38; /* Primary green */
  color: white;
  border: none;
  border-radius: 8px; /* Rounded corners */
  cursor: pointer;
  font-family: 'Nohemi', sans-serif; /* Use Nohemi font */
  font-weight: 600;
  font-size: 1rem;
  transition: background-color 0.2s ease;
  margin-top: 0.5rem;
}

button[type="submit"]:hover:not(:disabled) {
  background-color: #2e6b2c; /* Darker green */
}

button[type="submit"]:disabled {
  background-color: #9ccc65; /* Lighter green when disabled */
  cursor: not-allowed;
}

.error-message {
  color: #d32f2f; /* Red color for errors */
  background-color: #ffebee; /* Light red background */
  border: 1px solid #ef9a9a; /* Lighter red border */
  padding: 0.75rem;
  border-radius: 8px; /* Rounded corners */
  margin-top: 0.5rem;
  text-align: center;
  font-size: 0.9rem;
}

.switch-link {
  text-align: center;
  margin-top: 1.5rem;
  color: #555;
  font-size: 0.9rem;
}

.link-button { /* Style the register/login switch button like a link */
  background: none;
  border: none;
  color: #3c8a38; /* Primary green */
  text-decoration: underline;
  cursor: pointer;
  font-family: inherit; /* Use the same font as surrounding text */
  font-size: inherit;
  padding: 0;
  font-weight: 600;
}

.link-button:hover {
  color: #2e6b2c; /* Darker green */
}
</style>