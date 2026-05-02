import { useState, useEffect } from 'react';
import './index.css';

function App() {
  const [transcript, setTranscript] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [mode, setMode] = useState('single'); // 'single' or 'batch'

  useEffect(() => {
    if (analysis) {
      console.log('Analysis:', analysis);
    }
  }, [analysis]);

  const handleAnalyze = async () => {
    setLoading(true);
    setError(null);
    setAnalysis(null);

    try {
      let payload, endpoint;
      
      if (mode === 'batch') {
        const transcriptText = transcript.trim();
        if (!transcriptText) {
          throw new Error('Please enter transcripts');
        }
        
        let transcriptArray;

        try {
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

      Transcript(s):
      ${transcript}
      `;
        
        // Try parsing as JSON first
        try {
          const parsed = JSON.parse(transcriptText);
          if (parsed.transcripts && Array.isArray(parsed.transcripts)) {
            transcriptArray = parsed.transcripts.map(t => ({
              id: t.id || Math.random().toString(36).substr(2, 9),
              fellow: t.fellow || { name: t.fellow?.name || 'Unknown' },
              transcript: t.transcript
            }));
          } else {
            throw new Error('Invalid JSON format');
          }
        } catch (e) {
          // Not JSON - try delimited text
          const transcriptParts = transcriptText.split(/(?:^|\n)---+(?:$|\n)|(?:^|\n)TRANSCRIPT:+/i);
          const validTranscripts = transcriptParts
            .map(t => t.trim())
            .filter(t => t.length > 0);
          
          if (validTranscripts.length === 0) {
            throw new Error('Please enter at least one transcript');
          }
          
          transcriptArray = validTranscripts.map((t, idx) => ({
            transcript: t,
            fellow: { name: `Fellow ${idx + 1}` },
            id: Math.random().toString(36).substr(2, 9)
          }));
        }
        
        payload = { transcripts: transcriptArray };
        endpoint = 'http://localhost:5177/api/analyze';
        console.log(`Sending batch of ${transcriptArray.length} transcripts`);
        else {
        if (!transcript.trim()) {
          throw new Error('Please enter a transcript');
        }
        payload = { transcript };
        endpoint = 'http://localhost:5177/api/analyze_single';
        console.log('Sending single:', payload);
      }

      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP ${response.status}: ${errorText}`);
      }

      const data = await response.json();
      setAnalysis(mode === 'batch' ? data : [data]);
      
    } catch (err) {
      console.error('Error:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const renderList = (items) => {
    if (!items || !items.length) return <li>No items found</li>;
    return items.map((item, index) => (
      <li key={index}>
        {typeof item === 'object' ? item.detail || JSON.stringify(item) : item}
      </li>
    ));
  };

  const renderResultCard = (data, index = 0) => (
    <section key={index} className="results-card">
      <h2>Assessment Results {data.fellow_name ? `for ${data.fellow_name}` : ''}</h2>
      
      <div className="result-section">
        <h3>Overall Performance</h3>
        <div className="score-display">
          {data.score?.value || 'N/A'}/10
          <span className="score-label">{data.score?.label}</span>
          <span className="score-band">({data.score?.band})</span>
        </div>
        <p>{data.score?.justification}</p>
      </div>

      <div className="result-section">
        <h3>KPIs</h3>
        <ul>{renderList(data.kpis)}</ul>
      </div>

      <div className="result-section">
        <h3>Gaps</h3>
        <ul>{renderList(data.gaps)}</ul>
      </div>

      {data.questions && (
        <div className="result-section">
          <h3>Questions</h3>
          <ul>{renderList(data.questions)}</ul>
        </div>
      )}
    </section>
  );

  return (
    <div className="app-shell">
<header>
        <h1>DT Assessment System</h1>
        <p>DT Fellow Feedback Analyzer</p>
      </header>

      <section className="input-card">
        <div className="mode-toggle">
          <button 
            className={mode === 'single' ? 'active' : ''} 
            onClick={() => setMode('single')}
          >
            Single Transcript
          </button>
          <button 
            className={mode === 'batch' ? 'active' : ''} 
            onClick={() => setMode('batch')}
          >
            Batch Processing
          </button>
        </div>

        <textarea
          value={transcript}
          onChange={(e) => setTranscript(e.target.value)}
          placeholder={mode === 'batch' 
            ? "Paste JSON array or delimited transcripts..." 
            : "Paste supervisor transcript here..."
          }
        />

        <button onClick={handleAnalyze} disabled={loading}>
{loading ? 'Analyzing...' : 'Generate Assessment'}
        </button>
        {error && <div className="error">{error}</div>}
      </section>

      {analysis && (
        <div className="results-container">
          {Array.isArray(analysis) 
            ? analysis.map((item, idx) => renderResultCard(item, idx))
            : renderResultCard(analysis)
          }
        </div>
      )}
    </div>
  );
}}

export default App;
