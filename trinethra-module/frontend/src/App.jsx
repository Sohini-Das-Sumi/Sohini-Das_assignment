import { useState, useEffect } from 'react';
import './index.css';

function App() {
  const [transcript, setTranscript] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    console.log('Analysis state changed:', analysis);
    console.log('Analysis truthy?', !!analysis);
    if (analysis) {
      console.log('Analysis keys:', Object.keys(analysis));
      console.log('Score:', analysis.score);
    }
  }, [analysis]);

  async function handleAnalyze() {
    console.log('Starting analysis...');
    console.log('Raw transcript input:', transcript);
    console.log('Transcript type:', typeof transcript);

    if (!transcript.trim()) {
      console.log('No transcript provided');
      setError('Please paste a transcript first.');
      return;
    }

    // Check if transcript is JSON and extract text if needed
    let transcriptText = transcript;
    try {
      const parsed = JSON.parse(transcript);
      console.log('Parsed JSON:', parsed);
      if (parsed.transcripts && Array.isArray(parsed.transcripts)) {
        transcriptText = parsed.transcripts.map(t => t.text || t.transcript || JSON.stringify(t)).join(' ');
        console.log('Extracted text from JSON:', transcriptText);
      } else if (parsed.transcript) {
        transcriptText = parsed.transcript;
      } else if (typeof parsed === 'string') {
        transcriptText = parsed;
      }
    } catch (e) {
      console.log('Not JSON, using as plain text');
    }

    console.log('Final transcript text:', transcriptText.substring(0, 100) + '...');
    setError(null);
    setLoading(true);
    setAnalysis(null);

    try {
      console.log('Making fetch request to /api/analyze');
      const response = await fetch('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ transcript: transcriptText }),
      });

      console.log('Response status:', response.status);
      console.log('Response ok:', response.ok);

      if (!response.ok) {
        let errorMessage = 'Analysis failed.';
        try {
          const body = await response.json();
          console.log('Error response body:', body);
          errorMessage = body.error || errorMessage;
        } catch (e) {
          console.log('Failed to parse error response:', e);
          errorMessage = `Server error: ${response.status} ${response.statusText}`;
        }
        throw new Error(errorMessage);
      }

      const data = await response.json();
      console.log('Analysis data received:', data);
      console.log('Setting analysis state...');
      setAnalysis(data);
      console.log('Analysis set successfully');
    } catch (err) {
      console.error('Analysis error:', err);
      setError(err.message || 'An unexpected error occurred. Please try again.');
    } finally {
      setLoading(false);
      console.log('Loading set to false');
    }
  }

  const renderList = (items) => {
    if (!items || !items.length) {
      return <li>No items found.</li>;
    }
    return items.map((item, index) => {
      // Handle objects with detail property (like gaps)
      if (typeof item === 'object' && item.detail) {
        return <li key={index}>{item.detail}</li>;
      }
      // Handle strings
      return <li key={index}>{item}</li>;
    });
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
          placeholder="Paste the complete supervisor feedback transcript here for analysis. Supports both plain text and JSON format with transcripts array."
          aria-describedby="transcript-help"
        />
        <div id="transcript-help" className="help-text">
          Enter supervisor feedback as plain text or JSON format (with transcripts array). The system will automatically extract and analyze the content.
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
        <section key={Date.now()} className="results-card">
          {console.log('Rendering results section, analysis:', analysis)}
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
              {analysis.evidence && analysis.evidence.length ? (
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
