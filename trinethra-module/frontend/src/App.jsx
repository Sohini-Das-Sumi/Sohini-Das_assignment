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
        <p>Analyze supervisor transcripts to generate comprehensive performance assessments with evidence-based scoring and actionable insights.</p>
      </header>

      <section className="input-card">
        <h2>Transcript Analysis</h2>
        <label htmlFor="transcript">Supervisor Transcript</label>
        <textarea
          id="transcript"
          value={transcript}
          onChange={(event) => setTranscript(event.target.value)}
          placeholder="Paste the complete supervisor feedback transcript here for analysis..."
          aria-describedby="transcript-help"
        />
        <div id="transcript-help" className="help-text">
          Enter the full transcript of supervisor feedback for comprehensive analysis
        </div>
        <button onClick={handleAnalyze} disabled={loading} aria-describedby="button-help">
          {loading ? 'Analyzing Transcript...' : 'Generate Assessment'}
        </button>
        <div id="button-help" className="help-text">
          Click to analyze the transcript and generate a detailed performance assessment
        </div>
        {error && <div className="error">{error}</div>}
      </section>

      {analysis && (
        <section className="results-card">
          <h2>Assessment Results</h2>

          <div className="result-section">
            <h3>Overall Performance Score</h3>
            <div className="score-display">
              {analysis.score?.value ?? 'N/A'}/10
              {analysis.score?.label && <span className="score-label">{analysis.score.label}</span>}
            </div>
            {analysis.score?.band && <div className="score-band">Performance Band: {analysis.score.band}</div>}
            <p>{analysis.score?.justification ?? 'No justification provided.'}</p>
          </div>

          <div className="result-section">
            <h3>Evidence-Based Analysis</h3>
            <ul>
              {analysis.evidence?.length ? (
                analysis.evidence.map((item, index) => (
                  <li key={index} className="evidence-item">
                    <span className={`evidence-sentiment ${item.sentiment?.toLowerCase() || 'neutral'}`}>
                      {item.sentiment || 'Neutral'}
                    </span>
                    <span className="evidence-dimension">[{item.dimension || 'General'}]</span>
                    <div className="evidence-quote">"{item.quote}"</div>
                  </li>
                ))
              ) : (
                <li>No evidence extracted from the transcript.</li>
              )}
            </ul>
          </div>

          <div className="result-section">
            <h3>Key Performance Indicators</h3>
            <ul>{renderList(analysis.kpis)}</ul>
          </div>

          <div className="result-section">
            <h3>Development Gaps Identified</h3>
            <ul>{renderList(analysis.gaps)}</ul>
          </div>

          <div className="result-section">
            <h3>Recommended Follow-up Questions</h3>
            <ul>{renderList(analysis.questions)}</ul>
          </div>
        </section>
      )}
    </div>
  );
}

export default App;
