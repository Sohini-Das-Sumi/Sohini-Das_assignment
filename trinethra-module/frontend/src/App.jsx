import { useState, useEffect } from 'react';
import './index.css';
import { generatePrompt } from './prompt.js';

const renderList = (items, isEditable = false, onChange = null, itemPath = '') => {
  if (!items || !items.length) return <li>No items found</li>;
  return items.map((item, index) => {
    const keyPath = `${itemPath}.${index}`;
    const content = typeof item === 'object' ? item.detail || JSON.stringify(item) : item;
    if (isEditable) {
      return (
        <li key={index}>
          <input
            type="text"
            defaultValue={content}
            onBlur={(e) => onChange(keyPath, e.target.value)}
            className="edit-input"
          />
        </li>
      );
    }
    return <li key={index}>{content}</li>;
  });
};

const exportWordForCard = async (index, data, reviewState, reviewerName) => {
  console.log('=== EXPORT START ===');
  console.log('Index:', index);
  console.log('Data:', data);
  console.log('ReviewState:', reviewState);
  console.log('ReviewerName:', reviewerName);
  
  try {
    const payload = {
      analysis: [data],
      reviews: [reviewState],
      reviewerName: reviewerName || 'Anonymous',
      timestamp: new Date().toISOString()
    };
    
    console.log('Payload:', JSON.stringify(payload, null, 2));
    
    const response = await fetch('http://localhost:5000/api/export_word', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    
    console.log('Response status:', response.status);
    
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Export failed: ${response.status} - ${errorText}`);
    }
    
    const result = await response.json();
    console.log('Result keys:', Object.keys(result));
    const base64Data = result.docx_base64;
    console.log('Base64 length:', base64Data ? base64Data.length : 'MISSING');
    
    if (!base64Data) throw new Error('No document data');
    
    // Direct data URL download (reliable for binary)
    const dataUrl = `data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64,${base64Data}`;
    const link = document.createElement('a');
    link.href = dataUrl;
    link.download = `trinethra_fellow_${index + 1}_report.docx`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    console.log('=== EXPORT SUCCESS ===');
    alert(`Downloaded: trinethra_fellow_${index + 1}_report.docx (${Math.round(base64Data.length * 0.75 / 1024)} KB)`);
    
  } catch (error) {
    console.error('=== EXPORT ERROR ===', error);
    alert('Export failed: ' + error.message + '\nCheck Console F12.');
  }
};

const renderResultCard = (data, index, reviewState, updateReview, reviewerName) => {
  const { status = 'draft', edits = {}, rejectReason = '', reviewer = '' } = reviewState || {};
  const isEditing = status === 'editing';
  const isRejected = status === 'rejected';
  const isApproved = status === 'approved';

  const handleFieldChange = (path, value) => {
    updateReview(index, { ...reviewState, edits: { ...edits, [path]: value } });
  };

  const handleStatusChange = (newStatus) => {
    updateReview(index, { status: newStatus });
  };

  const saveReview = async () => {
    try {
      await fetch('http://localhost:5000/api/save_review', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          review: { ...reviewState, data: data },
          timestamp: new Date().toISOString()
        })
      });
      alert('Review saved!');
    } catch (e) {
      localStorage.setItem(`review_${index}`, JSON.stringify(reviewState));
      alert('Saved locally');
    }
  };

  return (
    <section key={index} className={`results-card ${isRejected ? 'rejected' : ''} ${isApproved ? 'approved' : ''}`}>
      <div className="card-header">
        <div className="card-left">
          <h2>{data.fellow_name ? `${data.fellow_name}'s Assessment` : 'Assessment Results'}</h2>
          <div className="status-badge">{status.toUpperCase()}</div>
        </div>
        <div className="card-right">
          <span className="card-reviewer">{reviewer || 'Set name above'}</span>
          <div className="review-actions">
            {!isEditing && !isApproved && !isRejected && (
              <button onClick={() => handleStatusChange('editing')} className="btn-edit" title="Edit">✏️</button>
            )}
            {isEditing && (
              <>
                <button onClick={() => handleStatusChange('draft')} className="btn-cancel" title="Cancel">❌</button>
                <button onClick={saveReview} className="btn-save" title="Save">💾</button>
              </>
            )}
            <button onClick={() => handleStatusChange(isRejected ? 'draft' : 'rejected')} className="btn-reject" title="Reject">
              {isRejected ? '↺' : '❌'}
            </button>
            <button onClick={() => handleStatusChange('approved')} className="btn-approve" disabled={isRejected} title="Approve">
              ✅
            </button>
            <button onClick={() => exportWordForCard(index, data, reviewState, reviewerName)} className="btn-word" title="Export Word Report">📄</button>
          </div>
        </div>
      </div>

      {isRejected && (
        <div className="reject-reason">
          <strong>Reject Reason:</strong>
          <textarea
            value={rejectReason}
            onChange={(e) => updateReview(index, { rejectReason: e.target.value })}
            placeholder="Enter rejection reason..."
            rows="2"
          />
        </div>
      )}

      <div className="result-section">
        <h3>Score</h3>
        <div className="score-display">
          <span 
            contentEditable={isEditing} 
            suppressContentEditableWarning 
            onBlur={(e) => handleFieldChange('score.value', e.target.textContent)}
          >
            {edits['score.value'] || data.score?.value || 'N/A'}
          </span>/10
          <span className="score-label">{edits['score.label'] || data.score?.label || 'N/A'}</span>
        </div>
        <p 
          contentEditable={isEditing} 
          suppressContentEditableWarning 
          onBlur={(e) => handleFieldChange('score.justification', e.target.textContent)}
        >
          {edits['score.justification'] || data.score?.justification || 'No justification'}
        </p>
      </div>

      <div className="result-section">
        <h3>KPIs</h3>
        <ul>{renderList(data.kpis || data.k, isEditing, handleFieldChange, 'kpis')}</ul>
      </div>

      <div className="result-section">
        <h3>Gaps</h3>
        <ul>{renderList(data.gaps || data.g, isEditing, handleFieldChange, 'gaps')}</ul>
      </div>

      {data.questions && (
        <div className="result-section">
          <h3>Questions</h3>
          <ul>{data.questions.map((q, idx) => (
            <li key={idx} 
                contentEditable={isEditing} 
                suppressContentEditableWarning 
                onBlur={(e) => handleFieldChange(`questions.${idx}`, e.target.textContent)}
            >
              {q}
            </li>
          ))}</ul>
        </div>
      )}

      <div className="result-section">
        <h3>Feedback</h3>
        <textarea
          value={edits.feedback || data.feedback || ''}
          onChange={(e) => handleFieldChange('feedback', e.target.value)}
          readOnly={!isEditing}
          rows="3"
          placeholder="Feedback content"
        />
      </div>

      <div className="result-section">
        <h3>Summary</h3>
        <textarea
          value={edits.transcript || data.transcript || ''}
          onChange={(e) => handleFieldChange('transcript', e.target.value)}
          readOnly={!isEditing}
          rows="6"
          className="scrollable"
        />
      </div>
    </section>
  );
};

function App() {
const [transcript, setTranscript] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [reviewerName, setReviewerName] = useState(localStorage.getItem('trinethra_reviewer') || '');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [mode, setMode] = useState('single');


  useEffect(() => {
    localStorage.setItem('trinethra_reviewer', reviewerName);
  }, [reviewerName]);

  useEffect(() => {
    const saved = localStorage.getItem('trinethra_reviews');
    if (saved) setReviews(JSON.parse(saved));
  }, []);

  useEffect(() => {
    if (analysis && reviews.length > 0) {
      localStorage.setItem('trinethra_reviews', JSON.stringify(reviews));
    }
  }, [reviews]);

  const updateReview = (index, newState) => {
    const newReviews = [...reviews];
    newReviews[index] = { ...newReviews[index], ...newState, reviewer: reviewerName };
    setReviews(newReviews);
  };

  const clearResults = () => {
    setAnalysis(null);
    setReviews([]);
    setError(null);
    setTranscript('');
    localStorage.removeItem('trinethra_reviews');
  };

  const exportCSV = () => {
    const headers = ['Fellow', 'Status', 'Score', 'Reviewer', 'RejectReason'];
    const rows = analysis.map((item, i) => {
      const r = reviews[i] || {};
      return [
        item.fellow_name || `Fellow ${i + 1}`,
        r.status || 'draft',
        r.edits?.['score.value'] || item.score?.value || '',
        r.reviewer || reviewerName,
        r.rejectReason || ''
      ];
    });

    const csvLines = [headers, ...rows].map(row => row.map(cell => `"${cell.toString().replace(/"/g, '""')}"`).join(','));
    const csvContent = csvLines.join('\n');
    
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'trinethra_reviews.csv';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    setTimeout(() => URL.revokeObjectURL(url), 100);
  };

  const handleAnalyze = async (rawData, currentMode) => {
    setLoading(true);
    setError(null);
    setAnalysis(null);
    setReviews([]);


    try {
    const transcriptText = rawData.trim();
      if (!transcriptText) {
        setError('Please paste supervisor feedback transcript (at least 10 chars). Example: "Fellow executes tasks well but lacks initiative."');
        setLoading(false);
        return;
      }

      let payload, endpoint = 'http://localhost:5000/api/analyze_single';
      if (currentMode === 'batch') {
        let transcripts = [];
        try {
          const parsed = JSON.parse(transcriptText);
          transcripts = parsed.transcripts || [parsed];
        } catch {
          const parts = transcriptText.split(/\n-{3,}/);
          transcripts = parts.map(t => ({ transcript: t.trim(), fellow_name: `Fellow ${parts.indexOf(t) + 1}` })).filter(t => t.transcript);
        }
        payload = { transcripts };
        endpoint = 'http://localhost:5000/api/analyze';
      } else {
        payload = { transcript: transcriptText };
      }

      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!response.ok) throw new Error(`API error ${response.status}`);
      const data = await response.json();
      const analysisData = Array.isArray(data) ? data : [data];

      // Auto-generate summaries for transcript
      const enhancedAnalysis = await Promise.all(
        analysisData.map(async (item) => {
          try {
            const summaryRes = await fetch('http://localhost:5000/api/generate_summary', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ transcript: item.transcript || '' })
            });
            const { summary } = await summaryRes.json();
            const enhancedTranscript = `Summary:\n${summary}`;
            return { ...item, transcript: enhancedTranscript };
          } catch (summaryErr) {
            console.warn('Summary generation failed:', summaryErr);
            return { ...item, transcript: `Summary unavailable` };
          }
        })
      );

      const initialReviews = enhancedAnalysis.map((_, i) => ({ 
        status: 'draft', 
        edits: { transcript: enhancedAnalysis[i].transcript }, 
        reviewer: reviewerName 
      }));
      setReviews(initialReviews);
      setAnalysis(enhancedAnalysis);
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
        <p>AI-powered supervisor feedback analyzer. Automatically scores Deep Thoughts Fellows 1-10 using performance rubric, extracts evidence/KPIs/gaps, generates summaries, and produces editable Word reports. Batch/single mode support.</p>
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
          placeholder={mode === 'batch' ? "JSON: {\"transcripts\":[{\"transcript\":\"text1\"},{\"transcript\":\"text2\"}]} or --- separated" : 'Paste supervisor feedback e.g. "Fellow is reliable executor (6/10). Good at tasks. Needs initiative (layer 2)."' }
          rows="8"
        />
        <button onClick={() => handleAnalyze(transcript, mode)} disabled={loading}>
          {loading ? 'Analyzing...' : 'Analyze'}
        </button>

        <div className="reviewer-section">
          <label>Reviewer Name:</label>
          <input 
            type="text" 
            value={reviewerName}
            onChange={(e) => setReviewerName(e.target.value)}
            placeholder="Your name"
          />
        </div>

        {error && <div className="error">{error}</div>}
        {analysis && (
          <div className="action-bar">
            <button onClick={exportCSV} className="btn-export">📊 Export CSV</button>
            <button onClick={clearResults} className="btn-clear">Clear All</button>
          </div>
        )}
      </section>

      {analysis && (
        <div className="results-container">
          {Array.isArray(analysis)
            ? analysis.map((item, idx) => renderResultCard(item, idx, reviews[idx], updateReview, reviewerName))
            : renderResultCard(analysis, 0, reviews[0], updateReview, reviewerName)
          }
        </div>
      )}
    </div>
  );
}

export default App;

