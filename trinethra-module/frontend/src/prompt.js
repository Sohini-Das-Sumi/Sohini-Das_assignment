export const generatePrompt = (transcript) => {
  return `Analyze the following transcript for a Deep Thoughts fellow assessment using the TRINETHRA methodology.

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
   - 1-3: Need Attention
   - 4-6: Productivity
   - 7-10: Performance
5. BIASES: Detect Helpfulness (takes off plate), Presence (always on floor), Halo (glowing love), Recency (past week/recently).

JSON Output Requirements:
{
  "fellow_name": "string",
  "score": { "value": number, "label": "string", "band": "string", "justification": "string" },
  "kpis": [{"name": "string", "score": number}],
  "gaps": [{"dimension": "string", "detail": "string"}],
  "questions": ["string"],
  "biases": ["string"],
  "layers": { "execution": boolean, "systems_building": boolean, "layer2_strength": number },
  "dimensions": { "[key]": boolean },
  "evidence": [{"quote": "string", "sentiment": "positive|negative|neutral", "dimension": "string"}]
}

Transcript:
${transcript}`;
};

export const generateSummaryPrompt = (transcript) => {
  return `Generate a concise 2-3 sentence summary (50-100 words) of this supervisor feedback transcript. Focus on:
- Key strengths mentioned
- Main gaps or concerns
- Overall sentiment and performance impression

Make it editable and neutral. Output only the plain text summary, no JSON.

Transcript:
${transcript}`;
};

