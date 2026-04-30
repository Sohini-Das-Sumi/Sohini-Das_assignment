import re
import json
from collections import Counter

try:
    from textblob import TextBlob
except ImportError:
    TextBlob = None

class TrinethraCore:
    """Handles text cleaning and normalization."""
    SPECIAL_CHARACTERS = r'[^a-zA-Z0-9\s.,!?\'"-]'
    
    def preprocess_text(self, text):
        if not text or not isinstance(text, str):
            return ""
        cleaned = re.sub(self.SPECIAL_CHARACTERS, '', text)
        standardized = cleaned.lower()
        normalized = re.sub(r'\s+', ' ', standardized).strip()
        return normalized

class TrinethraAssess:
    """Logic for DT Fellow performance evaluation."""
    
    POSITIVE_KEYWORDS = [
        'good', 'great', 'excellent', 'amazing', 'fantastic', 'wonderful', 'outstanding', 'superb',
        'reliable', 'trustworthy', 'helpful', 'valuable', 'useful', 'efficient', 'effective',
        'sincere', 'dedicated', 'committed', 'professional', 'proactive', 'initiative', 'hands-on',
        'happy', 'satisfied', 'pleased', 'glad', 'grateful', 'relieved', 'impressed',
        'best', 'strong', 'solid', 'improve', 'improved', 'saved', 'faster', 'better',
        'love', 'adore', 'appreciate', 'thank', 'thanks', 'perfect', 'flawless'
    ]
    
    NEGATIVE_KEYWORDS = [
        'bad', 'poor', 'terrible', 'awful', 'horrible', 'disappointing', 'inadequate', 'insufficient',
        'unreliable', 'untrustworthy', 'useless', 'ineffective', 'inefficient', 'careless',
        'lazy', 'slow', 'sloppy', 'inconsistent', 'unpredictable', 'unprofessional',
        'worried', 'concerned', 'upset', 'frustrated', 'annoyed', 'irritated', 'disappointed',
        'problem', 'issue', 'trouble', 'difficulty', 'struggle', 'fail', 'failed',
        'complaint', 'complain', 'reject', 'rejection', 'error', 'mistake', 'wrong',
        'worst', 'weak', 'lacking', 'missing', 'absent', 'late', 'delayed'
    ]

    NEGATORS = ['not', "n't", 'never', 'no', 'hardly', 'barely', 'rarely']

    # KPI, Layer, and Dimension keywords (omitted for brevity but kept in logic)
    KPI_KEYWORDS = {
        'lead_generation': ['new customers', 'new schools', 'leads', 'prospects'],
        'lead_conversion': ['closed', 'converted', 'signed'],
        'upselling': ['bigger', 'increased', 'selling more'],
        'cross_selling': ['additional', 'extra'],
        'nps': ['happy', 'satisfied', 'recommend'],
        'pat': ['waste', 'reduced', 'saved', 'profit'],
        'tat': ['faster', 'quicker', 'turnaround', 'speed'],
        'quality': ['rejection', 'defect', 'complaint', 'quality']
    }
    
    LAYER_1_KEYWORDS = ['helps', 'maintains', 'updates', 'handles', 'coordinates', 'assists', 'does', 'manages']
    LAYER_2_KEYWORDS = ['built', 'created', 'designed', 'started', 'set up', 'developed', 'automated', 'streamlined']
    
    DIMENSION_KEYWORDS = {
        'Driving Execution': ['task', 'delivers', 'on time', 'follow up', 'completes'],
        'Building Systems': ['system', 'tracker', 'sheet', 'template', 'process', 'automate'],
        'KPI Impact': ['faster', 'saved', 'reduced', 'increased', 'improved', 'metrics'],
        'Change Management': ['resistance', 'adopt', 'workers', 'floor team', 'compliance']
    }

    TASK_ABSORPTION_PHRASES = ['runs my', 'takes my calls', 'handles all my', 'takes over', 'doing raghav\'s']

    def assess_transcript(self, transcript):
        if not transcript or not isinstance(transcript, str):
            return {'error': 'Transcript is required', 'errors': ['Transcript is required']}
        
        text_lower = transcript.lower()
        
        # Core Detection
        evidence = self._extract_evidence(transcript)
        layers = self._detect_layers(text_lower)
        kpi_mapping = self._map_kpis_detailed(text_lower)
        dimensions = self._detect_dimensions(text_lower)
        
        # Scoring Logic
        score_data = self._calculate_score(text_lower, evidence, layers, dimensions)
        gaps = self._identify_gaps(dimensions, layers)
        questions = self._generate_follow_up_questions(gaps)
        
        return {
            'score': score_data,
            'evidence': evidence,
            'kpiMapping': kpi_mapping,
            'gaps': gaps,
            'followUpQuestions': questions
        }

    def _extract_evidence(self, transcript):
        sentences = re.split(r'[.!?]+', transcript)
        evidence = []
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 15: continue
            
            polarity = self._sentence_polarity(sentence)
            sentiment = 'positive' if polarity > 0.1 else 'negative' if polarity < -0.1 else 'neutral'
            
            evidence.append({
                'quote': sentence[:200],
                'sentiment': sentiment,
                'dimension': self._classify_dimension(sentence.lower())
            })
        return evidence[:6]

    def _classify_dimension(self, text):
        scores = {dim: sum(1 for kw in kws if kw in text) for dim, kws in self.DIMENSION_KEYWORDS.items()}
        return max(scores, key=scores.get) if any(scores.values()) else 'Driving Execution'

    def _detect_layers(self, text):
        l1 = sum(1 for kw in self.LAYER_1_KEYWORDS if kw in text)
        l2 = sum(1 for kw in self.LAYER_2_KEYWORDS if kw in text)
        return {'execution': l1 > l2, 'systems_building': l2 >= l1, 'layer2_strength': l2}

    def _map_kpis_detailed(self, text):
        mappings = []
        for kpi, kws in self.KPI_KEYWORDS.items():
            if any(kw in text for kw in kws):
                mappings.append({
                    'kpi': kpi.replace('_', ' ').title(),
                    'systemOrPersonal': 'system' if any(s in text for s in ['built', 'tracker', 'process']) else 'personal'
                })
        return mappings[:4]

    def _detect_dimensions(self, text):
        return {dim: any(kw in text for kw in kws) for dim, kws in self.DIMENSION_KEYWORDS.items()}

    def _sentence_polarity(self, sentence):
        if TextBlob:
            return TextBlob(sentence).sentiment.polarity
        return self._keyword_polarity(sentence)

    def _keyword_polarity(self, text):
        text_lower = text.lower()
        pos = sum(1 for kw in self.POSITIVE_KEYWORDS if kw in text_lower)
        neg = sum(1 for kw in self.NEGATIVE_KEYWORDS if kw in text_lower)
        if (pos + neg) == 0: return 0.0
        score = (pos - neg) / (pos + neg)
        return -score if any(n in text_lower for n in self.NEGATORS) else score

    def _calculate_score(self, text, evidence, layers, dimensions):
        # Basic scoring heuristics
        core_score = 5
        if layers['systems_building'] and layers['layer2_strength'] >= 2: core_score = 8
        elif any(kw in text for kw in ['noticed', 'found', 'identified']): core_score = 7
        elif sum(dimensions.values()) >= 2: core_score = 6
        
        # Caps
        if any(p in text for p in self.TASK_ABSORPTION_PHRASES): core_score = min(core_score, 6)
        
        labels = {5: 'Consistent Performer', 6: 'Reliable and Productive', 7: 'Problem Identifier', 8: 'Problem Solver'}
        return {
            'value': core_score,
            'label': labels.get(core_score, 'Consistent Performer'),
            'band': 'Performance' if core_score >= 7 else 'Productivity'
        }

    def _identify_gaps(self, dimensions, layers):
        gaps = []
        if not layers['systems_building']: gaps.append({'dimension': 'systems_building'})
        if not dimensions.get('Change Management'): gaps.append({'dimension': 'change_management'})
        return gaps

    def _generate_follow_up_questions(self, gaps):
        questions = []
        for gap in gaps:
            if gap['dimension'] == 'systems_building':
                questions.append({'question': 'If the Fellow took a week off, what would stop working?'})
        return questions[:3]

class TrinethraModule:
    """Analyzes supervisor feedback and returns structured insights."""
    
    TOPIC_KEYWORDS = {
        'execution': ['execution', 'task', 'completion', 'delivery'],
        'systems_building': ['system', 'process', 'framework', 'automation'],
        'kpi_impact': ['metrics', 'kpi', 'numbers', 'results'],
        'change_management': ['change', 'initiative', 'innovation', 'improve']
    }
    
    def __init__(self):
        # Use Assess keywords for sentiment fallback
        self.assessor = TrinethraAssess()

    def analyze_feedback(self, text):
        if not text or not isinstance(text, str):
            return {'sentiment_score': 0.5, 'topics': [], 'summary': 'No feedback provided.'}
        
        score = self._calculate_sentiment(text)
        topics = self._extract_topics(text)
        summary = self._generate_summary(text, score)
        
        return {
            'sentiment_score': round(score, 2),
            'topics': topics,
            'summary': summary
        }
    
    def _calculate_sentiment(self, text):
        if TextBlob:
            polarity = TextBlob(text).sentiment.polarity
        else:
            polarity = self.assessor._keyword_polarity(text)
        return (polarity + 1) / 2 # Scale 0 to 1

    def _extract_topics(self, text):
        text_lower = text.lower()
        topic_scores = {t: sum(text_lower.count(kw) for kw in kws) for t, kws in self.TOPIC_KEYWORDS.items()}
        sorted_topics = sorted(topic_scores.items(), key=lambda x: x[1], reverse=True)
        return [t for t, s in sorted_topics[:3] if s > 0]
    
    def _generate_summary(self, text, score):
        sentences = [s.strip() for s in re.split(r'[.!?]', text) if len(s.strip()) > 5]
        if not sentences: return "Feedback received."
        
        main_sentence = max(sentences, key=len)
        prefix = "Positive:" if score > 0.6 else "Critical:" if score < 0.4 else "Mixed:"
        return f"{prefix} {main_sentence[:120]}..."

if __name__ == '__main__':
    analyzer = TrinethraModule()
    sample = "He maintains production tracking, coordinates quality complaints, and helped optimize the machine layout. His execution is solid but hasn't yet shown systems thinking."
    result = analyzer.analyze_feedback(sample)
    print(json.dumps(result, indent=4))