import { useState, useEffect } from 'react';
import './index.css';
import { generatePrompt } from './prompt.js';

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
        <ul>{data.questions.map((question, idx) => <li key={idx}>{question}</li>)}</ul>
      </div>
    )}

    <div className="result-section">
      <h3>Recommendations</h3>
      <p>{data.recommendations}</p>
    </div>

    <div className="result-section">
      <h3>Feedback</h3>
      <p>{data.feedback}</p>
    </div>

    <div className="result-section">
      <h3>Transcript</h3>
      <p>{data.transcript}</p>
    </div>
  </section>
);

function App() {
  const [transcript, setTranscript] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [mode, setMode] = useState('single'); // 'single' or 'batch'

  const clearResults = () => {
    setAnalysis(null);
    setError(null);
    setTranscript('');
  };


  const handleAnalyze = async (rawData, currentMode) => {
  setLoading(true);
  setError(null);
  setAnalysis(null);

  try {
    const transcriptText = rawData.trim();
    if (!transcriptText) throw new Error('Please enter a transcript');

    let payload, endpoint;

    if (currentMode === 'batch') {
      // Parse JSON or delimited
      let transcriptArray;
      try {
        const parsed = JSON.parse(transcriptText);
        transcriptArray = parsed.transcripts || [parsed];
      } catch {
        const parts = transcriptText.split(/(?:^|\n)---+(?:$|\n)/i);
        transcriptArray = parts
          .map(t => t.trim())
          .filter(t => t)
          .map((t, i) => ({ id: i.toString(), fellow: { name: `Fellow ${i+1}` }, transcript: t }));
      }
      payload = { transcripts: transcriptArray };
      endpoint = 'http://localhost:5177/api/analyze';
    } else {
      payload = { transcript: transcriptText };
      endpoint = 'http://localhost:5177/api/analyze_single';
    }

    console.log('Endpoint:', endpoint, payload.transcripts?.length || 1);
    
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`${response.status}: ${errorText}`);
    }

    const data = await response.json();
    setAnalysis(Array.isArray(data) ? data : [data]);
    
  } catch (err) {
    setError(err.message);
  } finally {
    setLoading(false);
  }
};

  return (
    <div className="app-shell">
      <header>
        <h1>Trinethra</h1>
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

        <button onClick={() => handleAnalyze(transcript, mode)} disabled={loading}>
          {loading ? 'Analyzing...' : 'Generate Assessment'}
        </button>
        
        {error && <div className="error">{error}</div>}
        
        {analysis && (
          <button onClick={clearResults} className="clear-btn">
            Clear Results
          </button>
        )}
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
}

export default App;