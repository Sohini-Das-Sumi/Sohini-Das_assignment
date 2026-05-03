# Supervisor Feedback Analyzer (Trinethra)

[![Backend](https://img.shields.io/badge/Backend-Express.js%20+%20Python-blue)](https://expressjs.com/)
[![Frontend](https://img.shields.io/badge/Frontend-React%20+%20Vite-green)](https://vitejs.dev/)
[![LLM](https://img.shields.io/badge/LLM-Ollama%20mistral-orange)](https://ollama.com/)

Trinethra analyzes supervisor transcripts using a 1-10 performance rubric (rubric.json), extracting evidence, scores, KPIs, gaps, and follow-up questions via local LLM.

## 🚀 Quickstart / Setup (Development Process Step 1)

**Prerequisites**:
- Node.js ≥16
- Python 3.8+ (for trinethra.py/llm_chain.py)
- Ollama: Download from [ollama.com](https://ollama.com/)
```
ollama pull mistral:latest
ollama serve  # Run in background
```

**Backend** (Terminal 1):
```
cd trinethra-module/backend
npm install
npm start  # http://localhost:3001
```

**Frontend** (Terminal 2):
```
cd trinethra-module/frontend
npm install
npm run dev  # http://localhost:5173
```

**Python Components**: Run tests via `test_server.py` or `test_request.py` (deps: requests, ollama if separate).

Open [http://localhost:5173](http://localhost:5173), paste transcript, click \"Run Analysis\".

## 🏗️ Architecture (Dev Steps 2-3: Build & Integrate)

```
trinethra-module/
├── backend/              # Express API (/analyze), Python LLM chain (trinethra.py)
│   ├── index.js          # Loads rubric.json, crafts prompt, Ollama call
│   ├── trinethra.py      # TrinethraAssess: signals, scoring logic
│   ├── llm_chain.py      # LLM interaction
│   └── test_*.py         # Tests & feedback (test_feedback.csv)
├── frontend/             # React UI
│   └── src/App.jsx       # Input, results display
├── rubric.json           # 1-10 rubric (bands, dimensions: Execution/Systems/KPI/Change)
├── transcript.json       # Sample inputs
├── IMPLEMENTATION.md     # Detailed dev notes
└── README.md             # You're here!
```

**Flow**: Transcript → Frontend POST /analyze → Backend prompt w/ rubric → Ollama JSON → Parse (fallback regex) → Structured output (score, evidence, KPIs, gaps, questions).

## ✅ Testing (Dev Step 4: Validate)

- 4 sample tests passed (TODO.md): Scores 5-8, bias/KPI detection.
- Run `python backend/test_server.py` or load transcript.json samples.
- Expected: Score boundary 6vs7 (executor vs problem-finder).

## 📈 Development Process Timeline

1. **Setup**: Git init, Node projects, data (rubric/transcript).
2. **Backend**: Express API, Python processing (signals/KPIs/dimensions/bias), Ollama integration, error handling.
3. **Frontend**: React form, results sections (score/evidence/KPIs/gaps/questions).
4. **Integration & Test**: Full flow, 4 verified samples.
5. **Iteration**: Backups, tests; all TODOs ✅.

**Commits**: Initial setup → Core logic → UI → Polish.

## 🔧 Design Challenges Tackled

- **Structured JSON**: Prompt + parse + regex fallback.
- **Single Prompt MVP**: Fast, simple.
- **Local LLM**: Ollama mistral (temp=0.2).

## 🚀 Next Steps / Improvements (Future Dev)

- Prompt tuning w/ samples.
- UI: Quote highlights, side-by-side, edit evidence.
- Backend: Retries, multi-model, logging.
- More tests vs expected scores.

See [IMPLEMENTATION.md](IMPLEMENTATION.md) for details, [TODO.md](../TODO.md) for tasks.

## ✨ Key Features
- **AI + Rules Hybrid**: Ollama Mistral JSON + Python keyword/sentiment/bias detection (TrinethraAssess).
- **1-10 Rubric**: Bands (Productivity/Performance), dimensions (Execution/Systems/KPI/Change).
- **Outputs**: Score/label/justification, evidence (quote/sentiment/dim), KPIs/gaps/questions/biases/layers.
- **Batch Mode**: JSON/delimited transcripts.
- **Fallbacks**: Regex parsing, no-LLM mode.

## 📱 Screenshots
*(Add after running: frontend results view)*

```
Score: 7/10 Problem Identifier (Performance)
Evidence: "He built tracker" → positive, Building Systems
KPIs: TAT, Quality
Gaps: Change Management
Questions: "Floor worker response?"
```

## 🚀 Next Steps / Improvements (Future Dev)

- Prompt tuning w/ samples.
- UI: Quote highlights, side-by-side, edit evidence.
- Backend: Retries, multi-model, logging.
- More tests vs expected scores.

See [IMPLEMENTATION.md](IMPLEMENTATION.md) for details, [TODO.md](../TODO.md) for tasks.

## License
MIT

