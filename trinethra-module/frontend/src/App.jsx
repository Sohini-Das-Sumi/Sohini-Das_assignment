import { useState } from 'react';
import './index.css';

function App() {
  const [transcript, setTranscript] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function handleAnalyze() {
    if (!transcript.trim()) {
      setError('Please paste a transcript first.');
      return;
    }
    setError(null);
    setLoading(true);
    setAnalysis(null);

    try {
      const response = await fetch('http://localhost:3001/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ transcript }),
      });

      if (!response.ok) {
        const body = await response.json();
        throw new Error(body.error || 'Analysis failed.');
      }

      const data = await response.json();
      setAnalysis(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  const renderList = (items) => {
    if (!items || !items.length) {
      return <li>No items found.</li>;
    }
    return items.map((item, index) => <li key={index}>{item}</li>);
  };

  return (
    <div className="app-shell">
      <header>
        <h1>Supervisor Feedback Analyzer</h1>
        <p>Paste a supervisor transcript and generate a draft assessment.</p>
      </header>

      <section className="input-card">
        <label htmlFor="transcript">Transcript</label>
        <textarea
          id="transcript"
          value={transcript}
          onChange={(event) => setTranscript(event.target.value)}
          placeholder="Paste the supervisor transcript here"
        />
        <button onClick={handleAnalyze} disabled={loading}>
          {loading ? 'Analyzing...' : 'Run Analysis'}
        </button>
        {error && <div className="error">{error}</div>}
      </section>

      {analysis && (
        <section className="results-card">
          <div className="result-section">
            <h2>Rubric Score</h2>
            <p>
              <strong>{analysis.score?.value ?? 'N/A'}/10</strong>
              {analysis.score?.label && ` — ${analysis.score.label}`}
              {analysis.score?.band && ` (${analysis.score.band})`}
            </p>
            <p>{analysis.score?.justification ?? 'No justification provided.'}</p>
          </div>

          <div className="result-section">
            <h2>Extracted Evidence</h2>
            <ul>
              {analysis.evidence?.length ? (
                analysis.evidence.map((item, index) => (
                  <li key={index}>
                    <strong>{item.sentiment}</strong> [{item.dimension ?? 'General'}]: {item.quote}
                  </li>
                ))
              ) : (
                <li>No evidence extracted.</li>
              )}
            </ul>
          </div>

          <div className="result-section">
            <h2>KPI Mapping</h2>
            <ul>{renderList(analysis.kpis)}</ul>
          </div>

          <div className="result-section">
            <h2>Gap Analysis</h2>
            <ul>{renderList(analysis.gaps)}</ul>
          </div>

          <div className="result-section">
            <h2>Suggested Follow-up Questions</h2>
            <ul>{renderList(analysis.questions)}</ul>
          </div>
        </section>
      )}
    </div>
  );
}

export default App;
