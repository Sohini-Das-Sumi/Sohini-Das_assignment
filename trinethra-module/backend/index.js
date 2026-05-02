const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');
const { exec } = require('child_process');


const app = express();
const PORT = 3001;


app.use(cors());
app.use(express.json());

app.get(['/', '/test-route'], (req, res) => {
  if (req.path === '/') {
    res.send('Hello, World!');
  } else if (req.path === '/test-route') {
    // Your existing code for handling /test-route
    res.send('Server is running!');
  } else {
    res.status(404).send('Not Found');
  }
});

app.post('/analyze', async (req, res) => {
  const { transcript } = req.body;

  if (!transcript) {
    return res.status(400).json({ error: 'Transcript is required' });
  }
  
    const prompt = `Analyze the following supervisor transcript(s) for a Design Thinking (DT) fellow assessment using the TRINETHRA methodology.
    
    TRINETHRA METHODOLOGY RULES:
    1. LAYERS:
       - Execution (Layer 1): Keywords like helps, maintains, updates, handles, coordinates, assists.
       - Systems Building (Layer 2): Keywords like built, created, designed, set up, developed, automated, streamlined.
    2. DIMENSIONS:
       - Driving Execution: focus on tasks, delivery on time, follow ups.
       - Building Systems: focus on trackers, sheets, templates, processes.
       - KPI Impact: focus on speed, reduced waste, improved metrics.
       - Change Management: focus on resistance, adoption, workers, floor team.
    3. SCORING ALGORITHM (Score 1-10):
       - Lack of Initiative (always returns 5).
       - Problem Identification + System Creation (returns 8).
       - Problem Identification only (returns 7).
       - Systems Creation only (7 if >=2 dimensions, else 6).
       - Presence of Task Absorption (cap score at 6 regardless of other strengths).
       - Multi-Dimension (>=2 dimensions, returns 6).
    4. BANDS:
       - 1-3: Needs Attention
       - 4-6: Productivity
       - 7-10: Performance
    5. BIASES: Detect Helpfulness (takes off plate), Presence (always on floor), Halo (glowing love), Recency (past week/recently).

    JSON Output Requirements:
    - fellow_name: string
    - score: { value: number, label: string, band: string, justification: string }
    - kpis: Array<{ name: string, score: number }> (1-10 scale)
    - gaps: Array<{ dimension: string, detail: string }>
    - questions: Array<string> (based on gaps)
    - biases: Array<string>
    - layers: { execution: boolean, systems_building: boolean, layer2_strength: number }
    - dimensions: { [key: string]: boolean }
    - evidence: Array<{ quote: string, sentiment: 'positive'|'negative'|'neutral', dimension: string }>
    
    Transcript:
    ${transcript}`;
  


  try {
    // Call Python script with the transcript
    const pythonProcess = spawn('py', ['trinethra.py'], {
      cwd: __dirname,
      stdio: ['pipe', 'pipe', 'pipe']
    });

    // Send transcript to Python script
    pythonProcess.stdin.write(JSON.stringify({ prompt }));
    pythonProcess.stdin.end();

    let output = '';
    let errorOutput = '';

    pythonProcess.stdout.on('data', (data) => {
      output += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
      errorOutput += data.toString();
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        console.error('Python error:', errorOutput);
        return res.status(500).json({ error: 'Analysis failed', details: errorOutput });
      }

      try {
        const result = JSON.parse(output.trim());
        res.json(result);
      } catch (parseError) {
        console.error('JSON parse error:', output);
        res.status(500).json({ error: 'Failed to parse result' });
      }
    });

  } catch (error) {
    console.error('Spawn error:', error);
    res.status(500).json({ error: 'Server error' });
  }
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});

//
function buildPrompt(transcript) {
  // Your buildPrompt logic here if needed
  return `Your prompt template ${transcript}`; // Single semicolon
}

function parseJsonResponse(responseText) {
  try {
    return JSON.parse(responseText);
  } catch {
    const start = responseText.indexOf('{');
    const end = responseText.lastIndexOf('}');
    if (start >= 0 && end > start) {
      try {
        return JSON.parse(responseText.slice(start, end + 1));
      } catch (innerError) {
        console.error('Fallback JSON parse failed', innerError);
        return null;
      }
    }
    return null;
  }
}