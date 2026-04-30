const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

const app = express();
const PORT = 3001;

app.use(cors());
app.use(express.json());

app.post('/analyze', async (req, res) => {
  const { transcript } = req.body;

  if (!transcript) {
    return res.status(400).json({ error: 'Transcript is required' });
  }

  try {
    // Call Python script with the transcript
    const pythonProcess = spawn('py', ['trinethra.py'], {
      cwd: __dirname,
      stdio: ['pipe', 'pipe', 'pipe']
    });

    // Send transcript to Python script
    pythonProcess.stdin.write(JSON.stringify({ transcript }));
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
        console.error('Python script error:', errorOutput);
        return res.status(500).json({ error: 'Analysis failed', details: errorOutput });
      }

      try {
        const result = JSON.parse(output.trim());
        res.json(result);
      } catch (parseError) {
        console.error('JSON parse error:', parseError, 'Output:', output);
        res.status(500).json({ error: 'Failed to parse analysis result' });
      }
    });

  } catch (error) {
    console.error(error);
    res.status(500).json({ error: error.message || 'Failed to analyze transcript' });
  }
});

function buildPrompt(transcript) {
  const rubricSummary = rubricBands
    .map((band) => {
      const levelLines = band.levels
        .map((level) => `  - ${level.score}: ${level.label} — ${level.description}`)
        .join('\n');
      return `Band: ${band.band} (${band.range[0]}-${band.range[1]})\n${band.description}\n${levelLines}`;
    })
    .join('\n\n');

  return `You are helping a psychology intern analyze supervisor feedback for a Fellow. Use the rubric defined below and the KPI labels exactly as shown.

Rubric:
${rubricSummary}

KPI labels:
- ${kpiList.join('\n- ')}

Assessment dimensions:
- ${assessmentDimensions.join('\n- ')}

Analyze the following transcript and produce ONLY valid JSON with this exact schema:
{
  "evidence": [{
    "quote": "string",
    "sentiment": "positive|negative|neutral",
    "dimension": "Driving Execution|Building Systems|KPI Impact|Change Management"
  }],
  "score": {
    "value": number,
    "label": "string",
    "band": "string",
    "justification": "string"
  },
  "kpis": ["string"],
  "gaps": ["string"],
  "questions": ["string"]
}

If a field cannot be answered, return an empty array or null for that field. Do not include any text outside the JSON object.

Transcript:
${transcript}`;
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
      }
    }
    return null;
  }
}

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});