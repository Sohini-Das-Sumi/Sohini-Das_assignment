# Trinethra - Supervisor Feedback Analyzer 🧠📊

[![Backend](https://img.shields.io/badge/Backend-Python%20Flask-blue)](https://flask.palletsprojects.com/)
[![Frontend](https://img.shields.io/badge/Frontend-React%20Vite-green)](https://vitejs.dev/)
[![AI](https://img.shields.io/badge/AI-Ollama%20Mistral-orange)](https://ollama.com/)
[![Tests](https://img.shields.io/badge/Tests-Passed-brightgreen)](README.md#testing)

**Trinethra** analyzes supervisor feedback transcripts for DT Fellows using a 1-10 performance rubric. Extracts score, evidence, KPIs, gaps, biases, follow-up questions, **and now generates structured summaries** via local LLM + rule-based logic.

## ✨ Features
- Score (1-10 with band/label), evidence extraction, KPIs, gaps.
- **New**: Transcript summarization (`/api/generate_summary`).
- Batch/single mode, local-first (no cloud).

## 🚀 Quick Start
See [detailed installation](trinethra-module/README.md).

1. Install Ollama: `ollama pull mistral`
2. Terminal 1 (Backend): `cd trinethra-module/backend && python trinethra.py`
3. Terminal 2 (Frontend): `cd trinethra-module/frontend && npm i && npm run dev`
4. Open [localhost:5173](http://localhost:5173)

## 🏗️ Architecture
```
Transcript → React Frontend → Flask API (5000) → TrinethraAssess + Ollama → JSON (score/summary/etc.)
```

## Testing
`python trinethra-module/backend/test_server.py`

## 📚 Detailed Docs
- [Setup & Troubleshooting](trinethra-module/README.md)
- [Implementation](trinethra-module/IMPLEMENTATION.md)

**License**: MIT
