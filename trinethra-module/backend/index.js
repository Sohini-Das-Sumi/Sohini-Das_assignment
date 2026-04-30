const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3001;
const rubricFile = path.join(__dirname, '..', 'rubric.json');

const rubricData = JSON.parse(fs.readFileSync(rubricFile, 'utf8'));
const rubricBands = rubricData.rubric.bands;
const kpiList = rubricData.kpis.map((item) => item.label);
const assessmentDimensions = rubricData.assessmentDimensions.map((item) => item.label);

app.use(cors());
app.use(express.json());

app.post('/analyze', async (req, res) => {
  const { transcript } = req.body;

  if (!transcript) {
    return res.status(400).json({ error: 'Transcript is required' });
  }

  try {
    const prompt = buildPrompt(transcript);

    const response = await fetch('http://localhost:11434/api/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: 'mistral:latest',
        prompt,
        temperature: 0.2,
        max_tokens: 750,
        stream: false
      })
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Ollama API error: ${errorText}`);
    }

    const data = await response.json();
    const analysis = parseJsonResponse(data.response);

    if (!analysis) {
      throw new Error('Could not parse LLM response as JSON');
    }

    res.json(analysis);
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

  return `You are helping a psychology intern analyze supervisor feedback for a DT Fellow (early-career professional in 3-6 month placement). Use the rubric defined below.

CRITICAL SCORING RULES:
1. SUPERVISOR BIASES TO WATCH:
   - Helpfulness: "handles all my calls", "my right hand" = task absorption, NOT systems building (max 6)
   - Presence: "always on the floor" ≠ systems building
   - Halo: One big positive story can inflate score
2. TASK ABSORPTION vs SYSTEMS: If Fellow personally runs things (meetings, calls, schedules) and nothing continues if they leave = max 5-6. Real systems = trackers, SOPs, processes that persist.
3. 6 vs 7 BOUNDARY (MOST IMPORTANT):
   - Score 6: Executes tasks supervisor defines ("does everything I give him")
   - Score 7: Identifies problems supervisor hadn't noticed ("rejection rate higher on Mondays")
4. TRAP CASES - How to score:
   - Karthik (expect 6-7): Supervisor says "Very sincere" but "doesn't push back" = no initiative = ceiling at 6
   - Meena (expect 7-8): Supervisor critical "too much on laptop" BUT built order tracker, quantified rejection, saved shipment = Layer 2 = 7-8
   - Anil (expect 5-6): Glowing "my right hand" BUT handles calls/runs meetings = task absorption = cap at 6

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
