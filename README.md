# Trinethra - Supervisor Feedback Analyzer 🧠📊

[![Backend](https://img.shields.io/badge/Backend-Python%20Flask%20+%20Node.js-blue)](https://flask.palletsprojects.com/)
[![Frontend](https://img.shields.io/badge/Frontend-React%20Vite-green)](https://vitejs.dev/)
[![AI](https://img.shields.io/badge/AI-Ollama%20Mistral-orange)](https://ollama.com/)
[![License](https://img.shields.io/badge/License-MIT-brightgreen)](LICENSE)

**Trinethra** analyzes supervisor feedback transcripts for DT Fellows using a 1-10 performance rubric. Extracts score, evidence, KPIs, gaps, biases, and follow-up questions via local LLM + rule-based logic.

## ✨ Features
- **Structured Analysis**: Score (1-10 with band/label), evidence extraction (sentiment/dimension), KPIs, gaps.
- **AI-Powered**: Ollama Mistral for JSON output + Python keyword/sentiment fallback.
- **Dimensions**: Driving Execution, Building Systems, KPI Impact, Change Management.
- **Batch/Single Mode**: Handle multiple transcripts.
- **Local-First**: No cloud, runs offline.

## 🚀 Quick Start
1. Install [Ollama](https://ollama.com/) & `ollama pull mistral`.
2. Terminal 1: `cd trinethra-module/backend && npm i && npm start`
3. Terminal 2: `cd trinethra-module/frontend && npm i && npm run dev`
4. Open [localhost:5173](http://localhost:5173), paste transcript → Analyze!

See [detailed setup](trinethra-module/README.md).

## 🏗️ Architecture
```
Transcript → Frontend (React) → Backend API (Flask/Node) → TrinethraAssess (Python rules) + Ollama → JSON Results
```
- **rubric.json**: 1-10 bands (e.g., 6: Reliable/Productivity).
- Samples: [transcript.json](trinethra-module/transcript.json).

## 📱 Demo
Paste transcript → Get:
```
Score: 7/10 (Problem Identifier)
Evidence: ["quote", positive, Driving Execution]
KPIs: Lead Conversion, TAT
Gaps: Change Management
Questions: "How do floor workers respond?"
```

## Testing
- 4 samples verified (test_feedback.csv).
- `python trinethra-module/backend/test_server.py`

## 📈 Roadmap
- UI highlights, confidence scores, multi-model.
- See [IMPLEMENTATION.md](trinethra-module/IMPLEMENTATION.md).

## Contributing
Fork → Branch → PR. Issues welcome!

**License**: MIT

