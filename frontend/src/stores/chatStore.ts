// filepath: c:\Users\maksk\Desktop\TheHack\open_ai_hackathon_atlas\frontend\src\stores\chatStore.ts
import { ref } from 'vue';
import { defineStore } from 'pinia';
import { sendMessageToAgent } from '@/services/apiService'; // Import the API function

// Define the structure for a chat message (consistent with ChatMessage.vue)
export interface ChatMessage {
  id: string;
  text: string;
  sender: 'user' | 'ai';
  timestamp: Date;
  threadId?: string; // Optional: Store thread ID with the message if needed
}

// Helper to generate a unique thread ID (for testing: single digit)
function generateThreadId() {
  // Return a random single digit as a string for testing
  return Math.floor(Math.random() * 10).toString();
}

// Define the chat store
export const useChatStore = defineStore('chat', () => {
  // --- State ---
  const messages = ref<ChatMessage[]>([]); // Array to hold all chat messages
  const isLoading = ref(false); // Tracks if the AI is currently generating a response
  const currentThreadId = ref<string | null>(null); // Stores the ID for the current conversation thread
  const chatError = ref<string | null>(null); // To store errors related to sending/receiving messages

  // --- Actions ---

  // Start a new conversation (reset messages and thread ID)
  function startNewConversation() {
    messages.value = [];
    currentThreadId.value = generateThreadId();
    chatError.value = null;
    isLoading.value = false;
  }

  // Action to send a message from the user
  async function sendMessage(messageText: string) {
    // If no thread ID, generate one (first message in a conversation)
    if (!currentThreadId.value) {
      currentThreadId.value = generateThreadId();
    }

    // 1. Add user's message immediately to the list
    const userMessage: ChatMessage = {
      id: Date.now().toString() + '-user',
      text: messageText,
      sender: 'user',
      timestamp: new Date(),
      threadId: currentThreadId.value,
    };
    messages.value.push(userMessage);

    // 2. Set loading state and clear previous errors
    isLoading.value = true;
    chatError.value = null;

    try {
      // 3. Call the API service function
      // Pass the user's message and the current thread ID (if it exists)
      const response = await sendMessageToAgent(messageText, currentThreadId.value);

      // 4. Add AI's response to the list
      const aiMessage: ChatMessage = {
        id: Date.now().toString() + '-ai',
        text: response.response, // Use the 'response' field from the API result
        sender: 'ai',
        timestamp: new Date(),
        threadId: response.thread_id, // Store the thread ID from the response
      };
      messages.value.push(aiMessage);

      // 5. Update the current thread ID if it's not already set or has changed
      if (response.thread_id && response.thread_id !== currentThreadId.value) {
        currentThreadId.value = response.thread_id;
      }

    } catch (error: any) {
      // 6. Handle errors from the API call
      console.error('Error sending message:', error);
      chatError.value = error.message || 'Failed to get response from AI. Please try again.';
      // Optionally add an error message to the chat list
      messages.value.push({
        id: Date.now().toString() + '-error',
        text: `Error: ${chatError.value}`,
        sender: 'ai', // Or a special 'system' sender
        timestamp: new Date(),
        threadId: currentThreadId.value,
      });
    } finally {
      // 7. Turn off loading state regardless of success or failure
      isLoading.value = false;
    }
  }

  // Action to clear the chat history and thread ID (e.g., on logout)
  function clearChat() {
    messages.value = [];
    currentThreadId.value = null;
    chatError.value = null;
    isLoading.value = false; // Reset loading state as well
  }

  // --- Return state and actions ---
  return {
    messages,
    isLoading,
    currentThreadId,
    chatError,
    sendMessage,
    clearChat,
    startNewConversation, // Export the new function
  };
});