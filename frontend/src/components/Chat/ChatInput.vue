// filepath: c:\Users\maksk\Desktop\TheHack\open_ai_hackathon_atlas\frontend\src\components\chat\ChatInput.vue
<script setup lang="ts">
import { ref } from 'vue';

// Define props that the parent component (ChatView) can pass down
// We expect a 'disabled' prop to know if the input should be blocked (e.g., while AI is thinking)
const props = defineProps<{
  disabled: boolean;
}>();

// Define the event that this component can send up to the parent
// We'll emit 'sendMessage' with the message text as payload
const emit = defineEmits<{
  (e: 'sendMessage', message: string): void;
}>();

// Local state to hold the text currently typed in the input field
const inputText = ref('');

// Function to handle sending the message
function submitMessage() {
  const message = inputText.value.trim(); // Remove leading/trailing whitespace
  if (message && !props.disabled) { // Only send if there's text and not disabled
    emit('sendMessage', message); // Emit the event with the message
    inputText.value = ''; // Clear the input field
  }
}
</script>

<template>
  <div class="chat-input">
    <input
      type="text"
      v-model="inputText"
      placeholder="Type your message..."
      :disabled="props.disabled"
      @keyup.enter="submitMessage"
    />
    <button @click="submitMessage" :disabled="props.disabled || !inputText.trim()">
      Send
    </button>
  </div>
</template>

<style scoped>
.chat-input {
  display: flex;
  padding: 0.75rem;
  border-top: 1px solid #a2e59f; /* Light green separator line */
  background-color: #f8fbef; /* Light ivory background */
}

.chat-input input {
  flex-grow: 1; /* Take available space */
  padding: 0.5rem 0.75rem;
  border: 1px solid #a2e59f; /* Light green border */
  border-radius: 8px; /* Rounded corners */
  margin-right: 0.5rem;
  font-family: 'Switzer', sans-serif; /* Use Switzer font */
  font-weight: 300;
  color: #212121; /* Dark gray text */
  background-color: #ffffff; /* White background */
}

.chat-input input:focus {
  outline: none;
  border-color: #3c8a38; /* Primary green border on focus */
  box-shadow: 0 0 0 2px rgba(60, 138, 56, 0.2); /* Subtle glow on focus */
}

.chat-input input::placeholder {
  color: #bdbdbd; /* Lighter gray for placeholder */
}

.chat-input input:disabled {
  background-color: #eeeeee; /* Slightly grayed out when disabled */
  cursor: not-allowed;
}

.chat-input button {
  padding: 0.5rem 1rem;
  background-color: #3c8a38; /* Primary green */
  color: white;
  border: none;
  border-radius: 8px; /* Rounded corners */
  cursor: pointer;
  font-family: 'Nohemi', sans-serif; /* Use Nohemi font */
  font-weight: 600;
  transition: background-color 0.2s ease; /* Smooth hover effect */
}

.chat-input button:hover:not(:disabled) {
  background-color: #2e6b2c; /* Darker green on hover */
}

.chat-input button:disabled {
  background-color: #9ccc65; /* Lighter green when disabled */
  cursor: not-allowed;
}
</style>