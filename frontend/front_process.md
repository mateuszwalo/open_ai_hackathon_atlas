# Frontend Development Process: Vue.js Integration

This document outlines the step-by-step process for developing the Vue.js frontend for the AI project, ensuring smooth integration with the FastAPI backend and effective collaboration among team members.

## Phase 1: Setup & Initialization ✅

**Goal:** Establish the foundational structure and environment for the frontend project.

1.  **✅ Prerequisites:**
    *   IMPORTANT - Other Team member wont be installing Node.js and npm or yarn. I will take avantage of the ones installed on my machine. The dont need to see the frontend as the POC will be ran from my machine. This will streamline the development process and reduce setup time.
2.  **✅ Project Scaffolding:** (Assumed completed based on project structure)
    *   Navigate to the root directory of the repository in your terminal.
    *   Use Vite to create the Vue 3 project within the `frontend` directory:
        ```bash
        # Make sure you are NOT inside the frontend directory yet
        # npm create vue@latest frontend # (Command was likely run previously)
        ```
    *   Selections made during setup (based on `package.json` and config files):
        *   Project name: `frontend`
        *   TypeScript: Yes
        *   JSX Support: No
        *   Vue Router: Yes
        *   Pinia: Yes
        *   Vitest: Yes
        *   End-to-End Testing: No
        *   ESLint: Yes
        *   Prettier: Yes
3.  **✅ Install Dependencies:**
    *   Navigate into the new directory: `cd frontend`
    *   Install dependencies: `npm install` (Assumed completed)
4.  **✅ Version Control Setup:**
    *   The `frontend` directory is part of the main Git repository.
    *   `.gitignore` file in `frontend/` includes `node_modules/`, `dist/`, `.env*`. ✅
    *   Initial frontend structure committed. ✅ (Assumed)
5.  **✅ Environment Configuration:**
    *   `.env.development` created inside the `frontend` directory. ✅
    *   `VITE_API_BASE_URL` defined pointing to the backend (`http://localhost:8000`). ✅
    *   `.env*` files are in `.gitignore`. ✅
6.  **✅ Initial Run:**
    *   Development server started: `npm run dev` ✅
    *   Default Vue app viewable in the browser. ✅
7.  **✅ Documentation:**
    *   Main [`README.md`](c%3A%5CUsers%5Cmaksk%5CDesktop%5CTheHack%5Copen_ai_hackathon_atlas%5CREADME.md) updated with basic instructions for *local* frontend setup (`npm install && npm run dev`). ✅ (Assumed based on previous steps)

---

## Phase 2: Core Development - Building the Chat Interface

**Goal:** Create the basic chat UI, connect it to the backend API, and manage chat state.

1.  **✅ API Service Layer:**
    *   Installed `axios`: `npm install axios` ✅
    *   Created `frontend/src/services/apiService.ts`. ✅
    *   Configured `axios` to use `VITE_API_BASE_URL`. ✅
    *   Implemented `sendMessageToAgent` function in [`apiService.ts`](c%3A%5CUsers%5Cmaksk%5CDesktop%5CTheHack%5Copen_ai_hackathon_atlas%5Cfrontend%5Csrc%5Cservices%5CapiService.ts) to call the backend's `/agent` endpoint. ✅
2.  **✅ Basic UI Structure (Components & Views):**
    *   Cleaned up default scaffolded components/views. ✅ (Assumed)
    *   Created main view `frontend/src/views/ChatView.vue`. ✅
    *   Created core chat components:
        *   [`frontend/src/components/chat/ChatInput.vue`](c%3A%5CUsers%5Cmaksk%5CDesktop%5CTheHack%5Copen_ai_hackathon_atlas%5Cfrontend%5Csrc%5Ccomponents%5Cchat%5CChatInput.vue): Form with text input and send button. ✅
        *   [`frontend/src/components/chat/MessageList.vue`](c%3A%5CUsers%5Cmaksk%5CDesktop%5CTheHack%5Copen_ai_hackathon_atlas%5Cfrontend%5Csrc%5Ccomponents%5Cchat%5CMessageList.vue): Displays the list of messages. ✅
        *   [`frontend/src/components/chat/ChatMessage.vue`](c%3A%5CUsers%5Cmaksk%5CDesktop%5CTheHack%5Copen_ai_hackathon_atlas%5Cfrontend%5Csrc%5Ccomponents%5CChat%5CChatMessage.vue): Represents a single message. ✅
    *   Configured Vue Router ([`frontend/src/router/index.ts`](c%3A%5CUsers%5Cmaksk%5CDesktop%5CTheHack%5Copen_ai_hackathon_atlas%5Cfrontend%5Csrc%5Crouter%5Cindex.ts)) to map `/` to `ChatView.vue`. ✅
3.  **State Management (Pinia):** 👈 **NEXT STEP**
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
4.  **✅ Implement Chat Interface:**
    *   In [`ChatView.vue`](c%3A%5CUsers%5Cmaksk%5CDesktop%5CTheHack%5Copen_ai_hackathon_atlas%5Cfrontend%5Csrc%5Cviews%5CChatView.vue), use components (`ChatInput`, `MessageList`). ✅ (Currently using local state, will switch to Pinia)
    *   Pass `messages` and `isLoading` state to [`MessageList.vue`](c%3A%5CUsers%5Cmaksk%5CDesktop%5CTheHack%5Copen_ai_hackathon_atlas%5Cfrontend%5Csrc%5Ccomponents%5Cchat%5CMessageList.vue). ✅ (Currently using local state)
    *   Connect [`ChatInput.vue`](c%3A%5CUsers%5Cmaksk%5CDesktop%5CTheHack%5Copen_ai_hackathon_atlas%5Cfrontend%5Csrc%5Ccomponents%5Cchat%5CChatInput.vue) to trigger message sending logic in `ChatView.vue`. ✅ (Will connect to Pinia action)
    *   Display a loading indicator based on the `isLoading` state. ✅
5.  **✅ Styling:**
    *   Chosen basic CSS approach. ✅
    *   Applied styles based on [`styling.md`](c%3A%5CUsers%5Cmaksk%5CDesktop%5CTheHack%5Copen_ai_hackathon_atlas%5Cfrontend%5Cstyling.md) (colors, fonts, rounded corners) to components ([`App.vue`](c%3A%5CUsers%5Cmaksk%5CDesktop%5CTheHack%5Copen_ai_hackathon_atlas%5Cfrontend%5Csrc%5CApp.vue), [`ChatView.vue`](c%3A%5CUsers%5Cmaksk%5CDesktop%5CTheHack%5Copen_ai_hackathon_atlas%5Cfrontend%5Csrc%5Cviews%5CChatView.vue), [`ChatInput.vue`](c%3A%5CUsers%5Cmaksk%5CDesktop%5CTheHack%5Copen_ai_hackathon_atlas%5Cfrontend%5Csrc%5Ccomponents%5Cchat%5CChatInput.vue), [`MessageList.vue`](c%3A%5CUsers%5Cmaksk%5CDesktop%5CTheHack%5Copen_ai_hackathon_atlas%5Cfrontend%5Csrc%5Ccomponents%5Cchat%5CMessageList.vue), [`ChatMessage.vue`](c%3A%5CUsers%5Cmaksk%5CDesktop%5CTheHack%5Copen_ai_hackathon_atlas%5Cfrontend%5Csrc%5Ccomponents%5CChat%5CChatMessage.vue)). ✅
    *   Defined custom fonts in [`main.css`](c%3A%5CUsers%5Cmaksk%5CDesktop%5CTheHack%5Copen_ai_hackathon_atlas%5Cfrontend%5Csrc%5Cassets%5Cmain.css). ✅

---

## Phase 3: Refinement & Features

**Goal:** Improve the user experience, add features, and ensure robustness.

1.  **Error Handling:** Implement user-friendly error messages for API failures in the Pinia store and display them in the UI.
2.  **UI/UX Improvements:**
    *   Refine scrolling behavior in `MessageList.vue` (already implemented basic auto-scroll).
    *   Consider adding user/AI avatars to `ChatMessage.vue`.
    *   Improve timestamp formatting or placement if needed.
3.  **Input Validation:** Add basic checks on the user input in `ChatInput.vue` if necessary (e.g., prevent sending empty messages - already implemented).
4.  **Testing (Vitest):** Write unit tests for components (`ChatInput`, `MessageList`, `ChatMessage`), the Pinia store (`chatStore`), and the API service (`apiService`).
5.  **(Optional) User Context:** If user-specific data (like personality traits mentioned in [`backend/prompts.py`](c%3A%5CUsers%5Cmaksk%5CDesktop%5CTheHack%5Copen_ai_hackathon_atlas%5Cbackend%5Cprompts.py)) needs to be managed or displayed, plan how to fetch and store this (potentially another Pinia store).
6.  **(Optional) Authentication:** If needed later, implement login/logout flows.

---

**(Next Steps: Continuous Improvement & Deployment Prep)**
```

**Next Steps for Us:**

1.  **Implement Pinia Store:** Proceed with Phase 2, Step 3.
2.  **Refactor `ChatView.vue`:** Update `ChatView.vue` to use the Pinia store instead of local state for messages and loading status.
3.  **Continue to Phase 3:** Once the core chat functionality with Pinia is working, move on to refinements.