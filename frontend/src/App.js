import { useState, useEffect } from 'react';
import './index.css';

function App() {
  const [transcript, setTranscript] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

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
      const payload = { transcript };
      console.log('Sending:', payload);

      const response = await fetch('http://localhost:5177/api/analyze_single', {
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
      setAnalysis(data);
      
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
        <h1>🚀 Trinethra</h1>
        <p>Supervisor Feedback Analyzer</p>
      </header>

      <section className="input-card">
        <textarea
          value={transcript}
          onChange={(e) => setTranscript(e.target.value)}
          placeholder="Paste supervisor transcript here..."
        />
        <button onClick={handleAnalyze} disabled={loading}>
          {loading ? 'Analyzing...' : '🔍 Generate Assessment'}
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
}

export default App;
