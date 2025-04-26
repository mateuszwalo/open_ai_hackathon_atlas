<!-- filepath: c:\Users\maksk\Desktop\TheHack\open_ai_hackathon_atlas\frontend\src\views\RegisterView.vue -->
<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '@/stores/authStore'; // Import the auth store
import { useRouter } from 'vue-router'; // Import useRouter to navigate

const authStore = useAuthStore(); // Get an instance of the auth store
const router = useRouter(); // Get router instance

// Refs for username, password, and confirm password
const username = ref('');
const password = ref('');
const confirmPassword = ref(''); // Added for password confirmation

// Function called when the registration form is submitted
const handleRegister = async () => {
  // Basic check if passwords match
  if (password.value !== confirmPassword.value) {
    authStore.authError = "Passwords do not match."; // Set error in store
    return; // Stop the function if passwords don't match
  }
  // Call the register action from the auth store
  await authStore.register({ username: username.value, password: password.value });
  // The store action handles redirection on success/failure
};

// Function to navigate to the login page
const goToLogin = () => {
  router.push('/login'); // Navigate to the '/login' route
};
</script>

<template>
  <div class="auth-view">
    <h1>Register</h1>
    <!-- Form calls handleRegister when submitted -->
    <form @submit.prevent="handleRegister" class="auth-form">
      <div class="form-group">
        <label for="username">Username</label>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <div class="form-group">
        <label for="confirmPassword">Confirm Password</label>
        <input type="password" id="confirmPassword" v-model="confirmPassword" required />
      </div>
      <!-- Show error message from the store if it exists -->
      <div v-if="authStore.authError" class="error-message">
        {{ authStore.authError }}
      </div>
      <!-- Disable button while loading, change text -->
      <button type="submit" :disabled="authStore.isLoading">
        {{ authStore.isLoading ? 'Registering...' : 'Register' }}
      </button>
    </form>
    <!-- Link to switch to the login page -->
     <p class="switch-link">
      Already have an account? <button @click="goToLogin" class="link-button">Login here</button>
    </p>
  </div>
</template>

<style scoped>
/* Styles are identical to LoginView, copy them here for consistency */
.auth-view {
  max-width: 400px;
  margin: 4rem auto;
  padding: 2rem;
  border: 1px solid #a2e59f;
  border-radius: 8px;
  background-color: #ffffff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  font-family: 'Switzer', sans-serif;
}

h1 {
  font-family: 'Nohemi', sans-serif;
  color: #3c8a38;
  text-align: center;
  margin-bottom: 1.5rem;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
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
  border-radius: 8px;
  font-family: 'Switzer', sans-serif;
  font-size: 1rem;
  transition: border-color 0.2s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #3c8a38;
  box-shadow: 0 0 0 2px rgba(60, 138, 56, 0.2);
}

button[type="submit"] {
  padding: 0.7rem 1rem;
  background-color: #3c8a38;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-family: 'Nohemi', sans-serif;
  font-weight: 600;
  font-size: 1rem;
  transition: background-color 0.2s ease;
  margin-top: 0.5rem;
}

button[type="submit"]:hover:not(:disabled) {
  background-color: #2e6b2c;
}

button[type="submit"]:disabled {
  background-color: #9ccc65;
  cursor: not-allowed;
}

.error-message {
  color: #d32f2f;
  background-color: #ffebee;
  border: 1px solid #ef9a9a;
  padding: 0.75rem;
  border-radius: 8px;
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

.link-button {
  background: none;
  border: none;
  color: #3c8a38;
  text-decoration: underline;
  cursor: pointer;
  font-family: inherit;
  font-size: inherit;
  padding: 0;
  font-weight: 600;
}

.link-button:hover {
  color: #2e6b2c;
}
</style>