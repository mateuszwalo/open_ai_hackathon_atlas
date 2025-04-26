// filepath: c:\Users\maksk\Desktop\TheHack\open_ai_hackathon_atlas\frontend\src\services\apiService.ts
import axios from 'axios';

// Create an axios instance configured to talk to your backend.
// It automatically uses the URL 'http://localhost:8000' which you defined earlier.
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL, // Reads the backend URL from .env.development
  headers: {
    'Content-Type': 'application/json', // Tells the backend we're sending JSON data
  },
});

// This defines what the response from the backend should look like.
// Based on your backend/main.py, it expects an object with 'response' and 'thread_id'.
export interface AgentResponse {
  response: string;
  thread_id: string;
}

/**
 * Sends a message to the backend agent.
 * @param message The text message from the user.
 * @param threadId The current conversation thread ID (or null if it's the first message).
 * @returns A Promise that resolves with the agent's response.
 */
export const sendMessageToAgent = async (message: string, threadId: string | null): Promise<AgentResponse> => {
  try {
    // Prepare the data to send to the backend, matching the AgentInput model in main.py
    const payload = {
      message: message,
      thread_id: threadId || "" // Use the provided threadId, or an empty string if it's null
    };

    console.log('Sending payload to /agent:', payload); // Log what we're sending (for debugging)

    // Send a POST request to the '/agent' endpoint on your backend
    const response = await apiClient.post<AgentResponse>('/agent', payload);

    console.log('Received response from /agent:', response.data); // Log what we received (for debugging)

    // Return the data part of the response (which should match AgentResponse)
    return response.data;

  } catch (error) {
    // If anything goes wrong (network error, backend error), log it
    console.error('Error sending message to agent:', error);

    // Re-throw the error so the part of the code calling this function knows something went wrong
    // We can add more user-friendly error handling later in Phase 3
    throw error;
  }
};

/**
 * MOCK FUNCTION: Simulates logging in a user.
 * In a real app, this would send credentials to the backend /login endpoint.
 * @param credentials User's login details (e.g., { username: 'test', password: 'password' })
 * @returns A Promise that resolves with a mock user ID.
 */
export const loginUser = async (credentials: any): Promise<{ userId: number }> => {
  console.log('Mock API: Logging in with', credentials);
  // Simulate a network delay
  await new Promise(resolve => setTimeout(resolve, 500));
  // Simulate successful login - return a mock user ID
  // In a real app, you'd check credentials and get a real ID or token from the backend
  if (credentials.username && credentials.password) {
    return { userId: 123 }; // Example user ID
  } else {
    throw new Error('Mock API: Invalid credentials');
  }
};

/**
 * MOCK FUNCTION: Simulates registering a new user.
 * In a real app, this would send details to the backend /register endpoint.
 * @param details User's registration details (e.g., { username: 'new', password: 'password' })
 * @returns A Promise that resolves with a mock user ID.
 */
export const registerUser = async (details: any): Promise<{ userId: number }> => {
  console.log('Mock API: Registering with', details);
  // Simulate a network delay
  await new Promise(resolve => setTimeout(resolve, 500));
  // Simulate successful registration
  if (details.username && details.password) {
    return { userId: 456 }; // Example new user ID
  } else {
    throw new Error('Mock API: Invalid registration details');
  }
};