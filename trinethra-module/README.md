# Supervisor Feedback Analyzer (Trinethra)

[![Backend](https://img.shields.io/badge/Backend-Python%20Flask-blue)](https://flask.palletsprojects.com/)
[![Frontend](https://img.shields.io/badge/Frontend-React%20+%20Vite-green)](https://vitejs.dev/)
[![AI](https://img.shields.io/badge/AI-Ollama%20Mistral-orange)](https://ollama.com/)

Trinethra analyzes supervisor transcripts using a 1-10 performance rubric ([rubric.json](rubric.json)), extracting score, evidence, KPIs, gaps, biases, and follow-up questions. **Now includes transcript summarization**.

## 🔧 Installation Notes

### Prerequisites
- **Python 3.8+**
- **Node.js ≥18**
- **Ollama**: Download from [ollama.com](https://ollama.com/)
  ```
  ollama serve  # Run in background
  ollama pull mistral  # ~4GB, first time
  ```
  *Troubleshoot*: `ollama list` (check models), port 11434 free.

### Backend (Python - Recommended Virtualenv)
```
# Global or project root
pip install -r requirements.txt  # flask, flask-cors, textblob, etc.

# Virtualenv (best practice)
python -m venv venv
venv\\Scripts\\activate  # Windows
pip install -r requirements.txt
```

### Frontend (Node)
```
cd trinethra-module/frontend
npm ci  # Clean install
```

## 🚀 Quickstart

**Terminal 1 - Backend**:
```
cd trinethra-module/backend
python trinethra.py
```
*Expected*: `Trinethra Module: Ready on http://localhost:5000`

**Terminal 2 - Frontend**:
```
cd trinethra-module/frontend
npm run dev
```
*Expected*: `Local: http://localhost:5173` (proxies /api → :5000)

**Test UI**: Open http://localhost:5173, paste sample from [transcript.json](transcript.json).

## 🏗️ Project Structure
```
trinethra-module/
├── backend/
│   ├── trinethra.py          # Flask API + core TrinethraAssess
│   ├── summary_chain.py      # New: Summary generation
│   └── test_*.py             # Tests
├── frontend/src/             # React App.jsx
├── rubric.json               # Scoring bands
└── requirements.txt
```

## ✅ Testing

### Backend Endpoints
```
# Analysis
curl -X POST http://localhost:5000/api/analyze_single -H "Content-Type: application/json" -d "{\"transcript\":\"Anil is excellent\"}"

# New: Summary
curl -X POST http://localhost:5000/api/generate_summary -H "Content-Type: application/json" -d "{\"transcript\":\"test transcript text\"}"

# Python test
python backend/test_server.py
```

### Recent Fixes
- Robust `/api/generate_summary` with logging/fallback.
- Frontend UX: Empty input handling, better placeholders.

**Ports**: Backend 5000 | Frontend 5173 | Ollama 11434
