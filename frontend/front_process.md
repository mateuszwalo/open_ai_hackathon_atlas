# Frontend Development Process: Vue.js Integration

This document outlines the step-by-step process for developing the Vue.js frontend for the AI project, ensuring smooth integration with the FastAPI backend and effective collaboration among team members.

## Phase 1: Setup & Initialization

**Goal:** Establish the foundational structure and environment for the frontend project.

1.  **Prerequisites:**
    *   IMPORTANT - Other Team member wont be installing Node.js and npm or yarn. I will take avantage of the ones installed on my machine. The dont need to see the frontend as the POC will be ran from my machine. This will streamline the development process and reduce setup time.
2.  **Project Scaffolding:**
    *   Navigate to the root directory of the repository in your terminal.
    *   Use Vite to create the Vue 3 project within the `frontend` directory:
        ```bash
        # Make sure you are NOT inside the frontend directory yet
        npm create vue@latest frontend
        ```
    *   Follow the prompts. Recommended selections:
        *   Project name: `frontend`
        *   TypeScript: Yes
        *   JSX Support: No
        *   Vue Router: Yes
        *   Pinia: Yes
        *   Vitest: Yes
        *   End-to-End Testing: Playwright (or Cypress): No
        *   ESLint: Yes
        *   Prettier: Yes
    *   Oxlint: No
    *   Navigate into the new directory: `cd frontend`
    *   Install dependencies: `npm install`
3.  **Version Control Setup:**
    *   The `frontend` directory should already be part of the main Git repository.
    *   Verify/update the main `.gitignore` file in the repository root to include `frontend/node_modules/`, `frontend/dist/`, `frontend/.env*`. Ensure the `.gitignore` inside `frontend/` also covers these if needed.
    *   Commit the initial frontend structure:
        ```bash
        git add .
        git commit -m "feat: Initial scaffold of Vue.js frontend"
        # git push origin <your-branch-name> # Push when ready
        ```
4.  **Environment Configuration:**
    *   Create `.env.development` inside the `frontend` directory.
    *   Define `VITE_API_BASE_URL` pointing to the local address where Docker exposes the backend:
        ```env
        # filepath: c:\Users\maksk\Desktop\TheHack\open_ai_hackathon_atlas\frontend\.env.development
        VITE_API_BASE_URL=http://localhost:8000
        ```
    *   Access this in code via `import.meta.env.VITE_API_BASE_URL`.
    *   Ensure `.env*` files are in `.gitignore`.
5.  **Initial Run:**
    *   Start the development server: `npm run dev`
    *   Open the browser to the specified local address (e.g., `http://localhost:5173`) to see the default Vue app.
6.  **Documentation:**
    *   Update the main [`README.md`](c%3A%5CUsers%5Cmaksk%5CDesktop%5CTheHack%5Copen_ai_hackathon_atlas%5CREADME.md) with basic instructions for *local* frontend setup and running (mentioning Node.js prerequisites and `npm install && npm run dev` within the `frontend` directory). Clarify that this is separate from the Docker setup for the backend.

---

## Phase 2: Core Development - Building the Chat Interface

**Goal:** Create the basic chat UI, connect it to the backend API, and manage chat state.

1.  **API Service Layer:**
    *   Install an HTTP client like `axios`:
        ```bash
        npm install axios
        ```
    *   Create a service file to handle API calls (e.g., `frontend/src/services/apiService.ts`).
    *   Configure `axios` to use the `VITE_API_BASE_URL`.
    *   Implement a function to call the backend's `/agent` endpoint (defined in [`backend/main.py`](c%3A%5CUsers%5Cmaksk%5CDesktop%5CTheHack%5Copen_ai_hackathon_atlas%5Cbackend%5Cmain.py)), handling the `message` and `thread_id` parameters.
        ````typescript
        // filepath: c:\Users\maksk\Desktop\TheHack\open_ai_hackathon_atlas\frontend\src\services\apiService.ts
        import axios from 'axios';

        const apiClient = axios.create({
          baseURL: import.meta.env.VITE_API_BASE_URL,
          headers: {
            'Content-Type': 'application/json',
          },
        });

        export interface AgentResponse {
          response: string;
          thread_id: string;
        }

        export const sendMessageToAgent = async (message: string, threadId: string | null): Promise<AgentResponse> => {
          try {
            const payload = { message, thread_id: threadId || "" };
            console.log('Sending payload:', payload); // Debug log
            const response = await apiClient.post<AgentResponse>('/agent', payload);
            console.log('Received response:', response.data); // Debug log
            return response.data;
          } catch (error) {
            console.error('Error sending message to agent:', error);
            // Consider more robust error handling
            throw error;
          }
        };
        ````
2.  **Basic UI Structure (Components & Views):**
    *   Clean up the default scaffolded components/views in `frontend/src/components` and `frontend/src/views`.
    *   Create a main view for the chat interface (e.g., `frontend/src/views/ChatView.vue`).
    *   Create core chat components:
        *   `frontend/src/components/chat/ChatInput.vue`: Form with text input and send button.
        *   `frontend/src/components/chat/MessageList.vue`: Displays the list of messages.
        *   `frontend/src/components/chat/ChatMessage.vue`: Represents a single message (user or AI).
    *   Configure Vue Router (`frontend/src/router/index.ts`) to map a route (e.g., `/`) to `ChatView.vue`.
3.  **State Management (Pinia):**
    *   Define a Pinia store for chat state (e.g., `frontend/src/stores/chatStore.ts`).
    *   State properties: `messages` (array of message objects), `currentThreadId` (string or null), `isLoading` (boolean).
    *   Actions:
        *   `sendMessage(message: string)`:
            *   Set `isLoading` to true.
            *   Add the user's message to the `messages` array.
            *   Call the `sendMessageToAgent` service function with the message and `currentThreadId`.
            *   On success: Add the AI's response message to the `messages` array, update `currentThreadId` from the response.
            *   On error: Handle the error (e.g., show an error message).
            *   Set `isLoading` to false.
4.  **Implement Chat Interface:**
    *   In `ChatView.vue`, use the `chatStore`.
    *   Pass the `messages` state to `MessageList.vue`.
    *   Connect `ChatInput.vue` to trigger the `sendMessage` action in the store.
    *   Display a loading indicator based on the `isLoading` state.
5.  **Styling:**
    *   Choose and set up a styling approach - we are going with basic CSS
---

## Phase 3: Refinement & Features

**Goal:** Improve the user experience, add features, and ensure robustness.

1.  **Error Handling:** Implement user-friendly error messages for API failures.
2.  **UI/UX Improvements:** Enhance styling, add message timestamps, user/AI avatars, scrolling behavior for the message list.
3.  **Input Validation:** Basic checks on the user input.
4.  **Testing (Vitest):** Write unit tests for components, the Pinia store, and the API service.
5.  **(Optional) User Context:** If user-specific data (like personality traits mentioned in [`backend/prompts.py`](c%3A%5CUsers%5Cmaksk%5CDesktop%5CTheHack%5Copen_ai_hackathon_atlas%5Cbackend%5Cprompts.py)) needs to be managed or displayed, plan how to fetch and store this (potentially another Pinia store).
6.  **(Optional) Authentication:** If needed later, implement login/logout flows.

---

**(Next Steps: Continuous Improvement & Deployment Prep)**
```

**Next Steps for Us:**

1.  **Review:** Does this updated plan cover the necessary steps clearly?
2.  **Questions:** Are there any parts that are unclear or need more detail?
3.  **Adjustments:** Do you want to change the order, add/remove steps, or choose different tools (e.g., styling library)?

Let me know your thoughts, and we can refine this further before you start coding Phase 2.// filepath: c:\Users\maksk\Desktop\TheHack\open_ai_hackathon_atlas\frontend\front_process.md
# Frontend Development Process: Vue.js Integration

This document outlines the step-by-step process for developing the Vue.js frontend for the AI project, ensuring smooth integration with the FastAPI backend and effective collaboration among team members.

## Phase 1: Setup & Initialization

**Goal:** Establish the foundational structure and environment for the frontend project.

1.  **Prerequisites:**
    *   Ensure all team members have Node.js (LTS version recommended) and npm or yarn installed. Verify versions:
        ```bash
        node -v
        npm -v
        # or
        yarn -v
        ```
2.  **Project Scaffolding:**
    *   Navigate to the root directory of the repository in your terminal.
    *   Use Vite to create the Vue 3 project within the `frontend` directory:
        ```bash
        # Make sure you are NOT inside the frontend directory yet
        npm create vue@latest frontend
        ```
    *   Follow the prompts. Recommended selections:
        *   Project name: `frontend`
        *   TypeScript: Yes
        *   JSX Support: No
        *   Vue Router: Yes
        *   Pinia: Yes
        *   Vitest: Yes
        *   End-to-End Testing: Playwright (or Cypress)
        *   ESLint: Yes
        *   Prettier: Yes
    *   Navigate into the new directory: `cd frontend`
    *   Install dependencies: `npm install`
3.  **Version Control Setup:**
    *   The `frontend` directory should already be part of the main Git repository.
    *   Verify/update the main `.gitignore` file in the repository root to include `frontend/node_modules/`, `frontend/dist/`, `frontend/.env*`. Ensure the `.gitignore` inside `frontend/` also covers these if needed.
    *   Commit the initial frontend structure:
        ```bash
        git add .
        git commit -m "feat: Initial scaffold of Vue.js frontend"
        # git push origin <your-branch-name> # Push when ready
        ```
4.  **Environment Configuration:**
    *   Create `.env.development` inside the `frontend` directory.
    *   Define `VITE_API_BASE_URL` pointing to the local address where Docker exposes the backend:
        ```env
        # filepath: c:\Users\maksk\Desktop\TheHack\open_ai_hackathon_atlas\frontend\.env.development
        VITE_API_BASE_URL=http://localhost:8000
        ```
    *   Access this in code via `import.meta.env.VITE_API_BASE_URL`.
    *   Ensure `.env*` files are in `.gitignore`.
5.  **Initial Run:**
    *   Start the development server: `npm run dev`
    *   Open the browser to the specified local address (e.g., `http://localhost:5173`) to see the default Vue app.
6.  **Documentation:**
    *   Update the main [`README.md`](c%3A%5CUsers%5Cmaksk%5CDesktop%5CTheHack%5Copen_ai_hackathon_atlas%5CREADME.md) with basic instructions for *local* frontend setup and running (mentioning Node.js prerequisites and `npm install && npm run dev` within the `frontend` directory). Clarify that this is separate from the Docker setup for the backend.

---

## Phase 2: Core Development - Building the Chat Interface

**Goal:** Create the basic chat UI, connect it to the backend API, and manage chat state.

1.  **API Service Layer:**
    *   Install an HTTP client like `axios`:
        ```bash
        npm install axios
        ```
    *   Create a service file to handle API calls (e.g., `frontend/src/services/apiService.ts`).
    *   Configure `axios` to use the `VITE_API_BASE_URL`.
    *   Implement a function to call the backend's `/agent` endpoint (defined in [`backend/main.py`](c%3A%5CUsers%5Cmaksk%5CDesktop%5CTheHack%5Copen_ai_hackathon_atlas%5Cbackend%5Cmain.py)), handling the `message` and `thread_id` parameters.
        ````typescript
        // filepath: c:\Users\maksk\Desktop\TheHack\open_ai_hackathon_atlas\frontend\src\services\apiService.ts
        import axios from 'axios';

        const apiClient = axios.create({
          baseURL: import.meta.env.VITE_API_BASE_URL,
          headers: {
            'Content-Type': 'application/json',
          },
        });

        export interface AgentResponse {
          response: string;
          thread_id: string;
        }

        export const sendMessageToAgent = async (message: string, threadId: string | null): Promise<AgentResponse> => {
          try {
            const payload = { message, thread_id: threadId || "" };
            console.log('Sending payload:', payload); // Debug log
            const response = await apiClient.post<AgentResponse>('/agent', payload);
            console.log('Received response:', response.data); // Debug log
            return response.data;
          } catch (error) {
            console.error('Error sending message to agent:', error);
            // Consider more robust error handling
            throw error;
          }
        };
        ````
2.  **Basic UI Structure (Components & Views):**
    *   Clean up the default scaffolded components/views in `frontend/src/components` and `frontend/src/views`.
    *   Create a main view for the chat interface (e.g., `frontend/src/views/ChatView.vue`).
    *   Create core chat components:
        *   `frontend/src/components/chat/ChatInput.vue`: Form with text input and send button.
        *   `frontend/src/components/chat/MessageList.vue`: Displays the list of messages.
        *   `frontend/src/components/chat/ChatMessage.vue`: Represents a single message (user or AI).
    *   Configure Vue Router (`frontend/src/router/index.ts`) to map a route (e.g., `/`) to `ChatView.vue`.
3.  **State Management (Pinia):**
    *   Define a Pinia store for chat state (e.g., `frontend/src/stores/chatStore.ts`).
    *   State properties: `messages` (array of message objects), `currentThreadId` (string or null), `isLoading` (boolean).
    *   Actions:
        *   `sendMessage(message: string)`:
            *   Set `isLoading` to true.
            *   Add the user's message to the `messages` array.
            *   Call the `sendMessageToAgent` service function with the message and `currentThreadId`.
            *   On success: Add the AI's response message to the `messages` array, update `currentThreadId` from the response.
            *   On error: Handle the error (e.g., show an error message).
            *   Set `isLoading` to false.
4.  **Implement Chat Interface:**
    *   In `ChatView.vue`, use the `chatStore`.
    *   Pass the `messages` state to `MessageList.vue`.
    *   Connect `ChatInput.vue` to trigger the `sendMessage` action in the store.
    *   Display a loading indicator based on the `isLoading` state.
5.  **Styling:**
    *   Choose and set up a styling approach (e.g., basic CSS, Tailwind CSS). If using Tailwind:
        ```bash
        npm install -D tailwindcss postcss autoprefixer
        npx tailwindcss init -p
        ```
        *   Configure `tailwind.config.js` and `frontend/src/index.css`.
    *   Apply basic styles to make the chat interface usable.

---

## Phase 3: Refinement & Features

**Goal:** Improve the user experience, add features, and ensure robustness.

1.  **Error Handling:** Implement user-friendly error messages for API failures.
2.  **UI/UX Improvements:** Enhance styling, add message timestamps, user/AI avatars, scrolling behavior for the message list.
3.  **Input Validation:** Basic checks on the user input.
4.  **Testing (Vitest):** Write unit tests for components, the Pinia store, and the API service.
5.  **(Optional) User Context:** If user-specific data (like personality traits mentioned in [`backend/prompts.py`](c%3A%5CUsers%5Cmaksk%5CDesktop%5CTheHack%5Copen_ai_hackathon_atlas%5Cbackend%5Cprompts.py)) needs to be managed or displayed, plan how to fetch and store this (potentially another Pinia store).
6.  **(Optional) Authentication:** If needed later, implement login/logout flows.

---

**(Next Steps: Continuous Improvement & Deployment Prep)**
```

**Next Steps for Us:**

1.  **Review:** Does this updated plan cover the necessary steps clearly?
2.  **Questions:** Are there any parts that are unclear or need more detail?
3.  **Adjustments:** Do you want to change the order, add/remove steps, or choose different tools (e.g., styling library)?

Let me know your thoughts, and we can refine this further before you start coding Phase 2.