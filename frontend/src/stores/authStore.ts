// filepath: c:\Users\maksk\Desktop\TheHack\open_ai_hackathon_atlas\frontend\src\stores\authStore.ts
import { ref } from 'vue';
import { defineStore } from 'pinia';
import { useRouter } from 'vue-router';
import { loginUser, registerUser } from '@/services/apiService';
import { useChatStore } from '@/stores/chatStore'; // Import the chat store

// Define the store
export const useAuthStore = defineStore('auth', () => {
  // --- State ---
  // Check local storage for persisted login state (simple example)
  // This tries to remember if the user was logged in across browser refreshes
  const isLoggedIn = ref(localStorage.getItem('isLoggedIn') === 'true');
  const userId = ref<number | null>(Number(localStorage.getItem('userId')) || null);
  const authError = ref<string | null>(null); // To store login/registration errors
  const isLoading = ref(false); // To show loading state (like a spinner)

  const router = useRouter(); // Allows us to redirect the user

  // --- Actions ---

  // Login action: Called when the user tries to log in
  async function login(credentials: any) {
    isLoading.value = true; // Show loading indicator
    authError.value = null; // Clear previous errors
    try {
      // Call the (mock) API service
      const response = await loginUser(credentials);
      // Update state on success
      isLoggedIn.value = true;
      userId.value = response.userId;
      // Persist login state (simple example using browser's local storage)
      localStorage.setItem('isLoggedIn', 'true');
      localStorage.setItem('userId', String(response.userId));
      // Redirect to chat page after successful login
      router.push('/');
    } catch (error: any) {
      // Update error state on failure
      authError.value = error.message || 'Login failed. Please try again.';
      isLoggedIn.value = false;
      userId.value = null;
      localStorage.removeItem('isLoggedIn'); // Clear persisted state on error
      localStorage.removeItem('userId');
    } finally {
      isLoading.value = false; // Hide loading indicator
    }
  }

  // Register action: Called when the user tries to register
  async function register(details: any) {
    isLoading.value = true; // Show loading indicator
    authError.value = null; // Clear previous errors
    try {
      // Call the (mock) API service
      const response = await registerUser(details);
      // Update state on success (log them in immediately after register)
      isLoggedIn.value = true;
      userId.value = response.userId;
      localStorage.setItem('isLoggedIn', 'true');
      localStorage.setItem('userId', String(response.userId));
      // Redirect to chat page after successful registration
      router.push('/');
    } catch (error: any) {
      // Update error state on failure
      authError.value = error.message || 'Registration failed. Please try again.';
      isLoggedIn.value = false;
      userId.value = null;
      localStorage.removeItem('isLoggedIn');
      localStorage.removeItem('userId');
    } finally {
      isLoading.value = false; // Hide loading indicator
    }
  }

  // Logout action: Called when the user logs out
  function logout() {
    // It's okay to get the store instance here inside the action
    const chatStore = useChatStore();

    isLoggedIn.value = false;
    userId.value = null;
    authError.value = null;
    // Clear persisted state
    localStorage.removeItem('isLoggedIn');
    localStorage.removeItem('userId');

    // Clear the chat state
    chatStore.clearChat(); // Call the clearChat action from the chat store

    // Redirect to login page
    router.push('/login');
  }

  // --- Return state and actions ---
  // Make the state and actions available for components to use
  return {
    isLoggedIn,
    userId,
    authError,
    isLoading,
    login,
    register,
    logout,
  };
});