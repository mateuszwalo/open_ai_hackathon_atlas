# Sentio Platform: Personalized Psychological Support Agent (Hackathon Project)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) 

## 🚀 Overview

Sentio Platform is a proof-of-concept application developed during the OpenAI Warsaw Hackathon. It aims to provide personalized psychological support through an AI-powered chat interface. The system utilizes a multi-agent architecture built with LangGraph and OpenAI models to understand user issues, potentially tailor responses based on Big Five personality traits, and leverage external knowledge via vector search.

The core idea is to guide the user through an initial 
questionnaire, assess their needs, potentially determine their personality profile via a questionnaire, and then provide empathetic support and relevant information.

## ✨ Features

*   **AI Chat Interface:** Interact with an AI agent system via a web-based chat.
*   **Multi-Agent System (LangGraph):**
    *   **Supervisor Agent:** Initial point of contact, gathers context, routes to other agents.
    *   **Summary Agent:** Condenses the initial conversation for context transfer.
    *   **Emotional Agent:** Provides empathetic support and potentially utilizes vector search for relevant information.
*   **Personality Assessment:** Optional questionnaire to determine Big Five personality traits (Extraversion, Agreeableness, Conscientiousness, Neuroticism, Openness).
*   **Vector Search:** FAISS index integration for retrieving relevant information from documents (content of documents not specified in provided files).
*   **User Authentication:** Basic mock login and registration system.
*   **Journaling:** Mood tracking calendar interface (currently uses dummy data).
*   **Dockerized Environment:** Easy setup using Docker Compose for all backend services.

## 🏗️ Architecture

The project follows a client-server architecture:

1.  **Frontend (Vue.js):**
    *   Built with Vue 3, Vite, and TypeScript.
    *   Uses Pinia for state management (chat history, auth status, questionnaire).
    *   Provides the user interface (Chat, Login, Register, Questionnaire, Journal).
    *   Communicates with the backend via Axios.
    *   Includes styling based on provided guidelines (`styling.md`).
2.  **Backend (FastAPI):**
    *   Built with Python and FastAPI.
    *   Orchestrates the AI agent interactions using LangGraph.
    *   Interfaces with OpenAI API for language models.
    *   Connects to various databases for data persistence and caching.
    *   Serves the main API endpoint (`/agent`).
3.  **AI Core (LangGraph & OpenAI SDK):**
    *   Defines the flow and state transitions between different AI agents.
    *   Utilizes OpenAI models (e.g., `gpt-4.1-mini`, `gpt-4.1`) via the `openai-agents` library.
4.  **Databases & Storage:**
    *   **PostgreSQL:** Stores user credentials, questionnaire answers, and calculated Big Five scores (schema defined in `init.sql`).
    *   **MongoDB:** Likely intended for chat history or other document-based storage (presence defined in `docker-compose.yml`).
    *   **Neo4j:** Graph database, potential use for modeling relationships or user context (presence defined in `docker-compose.yml`).
    *   **Redis:** In-memory cache, potentially used by Celery or LangGraph checkpointing (presence defined in `docker-compose.yml`).

## 🛠️ Technology Stack

*   **Frontend:** Vue.js 3, Vite, TypeScript, Pinia, Axios, CSS
*   **Backend:** Python 3.10, FastAPI, LangGraph, OpenAI Agents SDK
*   **AI:** OpenAI API (GPT models), LangChain (embeddings, vector stores)
*   **Databases:** PostgreSQL, MongoDB, Neo4j, Redis
*   **Containerization:** Docker, Docker Compose


## ⚙️ Setup and Installation

1.  **Prerequisites:**
    *   Docker and Docker Compose installed.
    *   Git installed.
    *   Node.js and npm installed (for frontend development/testing outside Docker).
    *   An OpenAI API Key with sufficient credits.

2.  **Clone the Repository:**
    ```bash
    git clone https://github.com/mateuszwalo/open_ai_hackathon_atlas
    cd <repository-directory>
    ```

3.  **Configure Environment Variables:**
    *   Locate the `.env` file in the project root.
    *   **Crucially, ensure your `OPENAI_API_KEY` is correctly set.**
    *   Verify the database credentials and connection details. The defaults should work with the Docker Compose setup.

4.  **Build and Run Docker Containers:**
    *   From the project root directory, run:
        ```bash
        docker-compose up -d --build
        ```
    *   This command will build the backend image and start all services (backend, postgres, mongo, neo4j, redis) in detached mode.


## ▶️ Running the Application

*   **Backend API:** Accessible at `http://localhost:8000`
*   **Neo4j Browser:** Accessible at `http://localhost:7474` (Login: `neo4j`, Password: `strongpassword1234`)
*   **PostgreSQL:** Accessible at `localhost:5432`
*   **MongoDB:** Accessible at `localhost:27017`

*   **Frontend (Development):**
    *   Navigate to the `frontend` directory: `cd frontend`
    *   Install dependencies: `npm install`
    *   Start the development server: `npm run dev`
    *   Access the frontend application in your browser, usually at `http://localhost:5173`.

## 🚀 Usage

1.  Open your browser and navigate to the frontend URL (e.g., `http://localhost:5173`).
2.  Register a new user or log in with existing credentials (currently uses mock authentication).
3.  If it's your first time, you'll be prompted to complete the personality questionnaire.
4.  Once logged in and the questionnaire is complete (or skipped via backend logic), you can access the main chat interface.
5.  Use the chat input to interact with the Atlas AI agent.
6.  Explore the Journal view via the sidebar.

**API Testing (Example):**
You can test the backend API directly using `curl`:
```bash
curl -X POST http://localhost:8000/agent \
   -H "Content-Type: application/json" \
   -d '{"message": "Hello, I feel a bit overwhelmed today.", "thread_id": ""}'
   
   
   
Project Structure 

├── backend/              
│   ├── database/         
│   ├── vector/           
│   ├── agents_logic.py   
│   ├── db.py             
│   ├── langgraph_config.py 
│   ├── main.py           
│   ├── prompts.py        
│   ├── states.py         
│   └── utils.py          
├── frontend/            
│   ├── public/       
│   ├── src/             
│   │   ├── assets/      
│   │   ├── components/   
│   │   ├── router/      
│   │   ├── services/    
│   │   ├── stores/       
│   │   ├── views/        
│   │   ├── App.vue       
│   │   └── main.ts      
│   ├── .env.development  
│   ├── index.html       
│   ├── package.json     
│   ├── tsconfig.json     
│   └── vite.config.ts   
├── .env                 
├── docker-compose.yml    
├── Dockerfile           
├── requirements.txt     