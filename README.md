# Supervisor Feedback Analyzer

## Setup Instructions

1. Ensure you have Node.js installed (version 16 or higher).
2. Install Ollama from [ollama.com](https://ollama.com/) and pull a model:
   ```
   ollama pull mistral:latest
   ```
3. Clone or navigate to the project directory.
4. Set up the backend:
   ```
   cd backend
   npm install
   npm start
   ```
5. Set up the frontend (in a new terminal):
   ```
   cd frontend
   npm install
   npm run dev
   ```
6. Open your browser to `http://localhost:5173` for the frontend, and ensure the backend is running at `http://localhost:3001`.

## Architecture Overview

- **Frontend:** React + Vite app for user interface (input transcript, display analysis).
- **Backend:** Express server that handles API requests and communicates with Ollama local HTTP API.
- **Ollama:** Local LLM for processing transcripts using the `mistral:latest` model.

## Design Challenges Tackled

1. **Structured Output Reliability:** Used JSON parsing with fallback extraction to handle inconsistent LLM responses.
2. **One Prompt or Many:** Opted for a single comprehensive prompt for this MVP to keep the workflow fast and simple.

## Improvements with More Time

- Add evidence linking to highlight quotes in the transcript.
- Implement multiple prompts for better accuracy in gap detection.
- Enhance UI with side-by-side view of transcript and analysis.