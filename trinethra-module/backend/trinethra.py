import re
import json

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

    BIAS_INDICATORS = {
        'helpfulness': ['handles all', 'takes off my plate', 'big relief', 'helper', 'does everything', 'relieves', 'my right hand', "don't know how we managed"],
        'presence': ['always on', 'on the floor', 'physically', 'present', 'never leaves'],
        'halo': ['love', 'glowing', 'amazing', 'fantastic', 'couldn\'t manage without'],
        'recency': ['last week', 'recently', 'lately', 'these days', 'past few']
    }

    TASK_ABSORPTION_PHRASES = ['runs my', 'takes my calls', 'handles all my', 'takes over', 'doing raghav\'s']

    def assess_transcript(self, transcript):
        if not transcript or not isinstance(transcript, str):
            return {'error': 'Transcript is required', 'errors': ['Transcript is required']}

        text_lower = transcript.lower()

        evidence = self._extract_evidence(transcript)
        layers = self._detect_layers(text_lower)
        kpis = self._map_kpis(text_lower)
        dimensions = self._detect_dimensions(text_lower)

        score = self._calculate_score(text_lower, evidence, layers, dimensions)
        gaps = self._identify_gaps(dimensions, layers, evidence)
        questions = self._generate_questions(gaps, dimensions)
        biases = self._detect_biases(text_lower)

        return {
            'score': score,
            'evidence': evidence,
            'kpis': kpis,
            'dimensions': dimensions,
            'gaps': gaps,
            'questions': questions,
            'biases': biases,
            'layers': layers
        }

    def _extract_evidence(self, transcript):
        sentences = re.split(r'[.!?]+', transcript)
        evidence = []

        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 20:
                continue

            polarity = self._sentence_polarity(sentence)
            if polarity > 0.1:
                sentiment = 'positive'
            elif polarity < -0.1:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'

            dimension = self._classify_dimension(sentence.lower())

            evidence.append({
                'quote': sentence[:200],
                'sentiment': sentiment,
                'dimension': dimension
            })

        return evidence[:6]

    def _classify_dimension(self, text):
        scores = {}

        for dim, keywords in self.DIMENSION_KEYWORDS.items():
            count = sum(1 for kw in keywords if kw in text)
            scores[dim] = count

        if not scores or max(scores.values()) == 0:
            return 'Driving Execution'

        return max(scores, key=scores.get)

    def _detect_layers(self, text):
        layer1_score = sum(1 for kw in self.LAYER_1_KEYWORDS if kw in text)
        layer2_score = sum(1 for kw in self.LAYER_2_KEYWORDS if kw in text)

        return {
            'execution': layer1_score > layer2_score,
            'systems_building': layer2_score >= layer1_score,
            'layer2_strength': layer2_score
        }

    def _map_kpis(self, text):
        matched_kpis = []

        for kpi, keywords in self.KPI_KEYWORDS.items():
            if any(kw in text for kw in keywords):
                matched_kpis.append(kpi.replace('_', ' ').title())

        return matched_kpis[:4]

    def _detect_dimensions(self, text):
        dimensions = {}

        for dim, keywords in self.DIMENSION_KEYWORDS.items():
            present = any(kw in text for kw in keywords)
            dimensions[dim] = present

        return dimensions

    def _sentence_polarity(self, sentence):
        if TextBlob is not None:
            try:
                return TextBlob(sentence).sentiment.polarity
            except Exception:
                pass
        return self._keyword_polarity(sentence)

    def _keyword_polarity(self, text):
        text_lower = text.lower()
        positive_count = sum(1 for kw in self.POSITIVE_KEYWORDS if kw in text_lower)
        negative_count = sum(1 for kw in self.NEGATIVE_KEYWORDS if kw in text_lower)
        total = positive_count + negative_count
        if total == 0:
            return 0.0
        return (positive_count - negative_count) / total

    def _calculate_score(self, text, evidence, layers, dimensions):
        has_task_absorption = any(phrase in text for phrase in self.TASK_ABSORPTION_PHRASES)
        problem_identifier_phrases = ['noticed', 'found that', 'discovered', 'identified', 'quantified', 'tracked', 'analysis']
        has_problem_id = any(phrase in text for phrase in problem_identifier_phrases)
        has_system_creation = layers['systems_building'] and layers['layer2_strength'] >= 2
        lack_initiative = ['doesn\'t push back', 'doesn\'t question', 'just does', 'no initiative', 'does what i tell', 'tells him to do']
        has_lack_initiative = any(phrase in text for phrase in lack_initiative)
        dimension_count = sum(dimensions.values())

        if has_lack_initiative:
            core_score = 5
        elif has_problem_id and has_system_creation:
            core_score = 8
        elif has_problem_id:
            core_score = 7
        elif has_system_creation:
            core_score = 7 if dimension_count >= 2 else 6
        elif dimension_count >= 2:
            core_score = 6
        else:
            core_score = 5

        if has_task_absorption and core_score > 6:
            core_score = 6
        if has_lack_initiative and core_score > 6:
            core_score = 6

        if core_score <= 3:
            band = 'Need Attention'
            label = 'Motivated but Directionless' if core_score == 3 else 'Consistent Performer'
        elif core_score <= 6:
            band = 'Productivity'
            labels = {4: 'Careless and Inconsistent', 5: 'Consistent Performer', 6: 'Reliable and Productive'}
            label = labels.get(core_score, 'Consistent Performer')
        else:
            band = 'Performance'
            labels = {7: 'Problem Identifier', 8: 'Problem Solver', 9: 'Innovative and Experimental', 10: 'Exceptional Performer'}
            label = labels.get(core_score, 'Problem Identifier')

        justification = self._generate_justification(core_score, text, layers, dimensions)

        return {
            'value': core_score,
            'label': label,
            'band': band,
            'justification': justification
        }

    def _generate_justification(self, score, text, layers, dimensions):
        justifications = {
            5: "Shows reliable task execution but limited systems building.",
            6: "Consistent performer with some operational responsibilities.",
            7: "Shows problem identification with evidence of tracking or analysis.",
            8: "Demonstrates systems building with tools or processes created."
        }

        base = justifications.get(score, "Mixed evidence in transcript.")

        if not layers['systems_building']:
            base += " No clear systems building detected."

        if not dimensions.get('Change Management', False):
            base += " No change management evidence present."

        return base

    def _identify_gaps(self, dimensions, layers, evidence):
        gaps = []

        if not layers['systems_building']:
            gaps.append({'dimension': 'systems_building', 'detail': 'No evidence of systems, processes, or tools created'})

        if not dimensions.get('Change Management', False):
            gaps.append({'dimension': 'change_management', 'detail': 'No mention of how Fellow handles resistance or gets team adoption'})

        if not dimensions.get('KPI Impact', False):
            gaps.append({'dimension': 'kpi_impact', 'detail': 'No measurable business outcome connections'})

        if not dimensions.get('Building Systems', False):
            gaps.append({'dimension': 'building_systems', 'detail': 'No structures, trackers, or SOPs documented'})

        return gaps

    def _generate_questions(self, gaps, dimensions):
        questions = []

        for gap in gaps:
            dim = gap['dimension']

            if dim == 'systems_building':
                questions.append('If the Fellow took a week off, what would stop working? What would keep running on its own?')
            elif dim == 'change_management':
                questions.append('How do the floor workers respond when the Fellow asks them to do something differently?')
            elif dim == 'kpi_impact':
                questions.append('Since the Fellow started, has any specific number improved — speed, complaints, rejections?')
            elif dim == 'building_systems':
                questions.append('Has the Fellow built anything that your team uses regularly after they leave?')

        if len(questions) < 3:
            questions.append('When was the last time the Fellow suggested a new approach or process?')

        return questions[:3]

    def _detect_biases(self, text):
        detected_biases = []

        for bias, indicators in self.BIAS_INDICATORS.items():
            if any(ind in text for ind in indicators):
                detected_biases.append(bias)

        return detected_biases

    def analyze_sentiment_keywords(self, text):
        text_lower = text.lower()

        positive_count = sum(1 for kw in self.POSITIVE_KEYWORDS if kw in text_lower)
        negative_count = sum(1 for kw in self.NEGATIVE_KEYWORDS if kw in text_lower)
        keywords_found = []

        for kw in self.POSITIVE_KEYWORDS:
            if kw in text_lower:
                keywords_found.append({'keyword': kw, 'type': 'positive'})

        for kw in self.NEGATIVE_KEYWORDS:
            if kw in text_lower:
                keywords_found.append({'keyword': kw, 'type': 'negative'})

        has_negation = any(neg in text_lower for neg in self.NEGATORS)
        total = positive_count + negative_count

        if total == 0:
            return {
                'score': 0.5,
                'label': 'neutral',
                'keywords_found': [],
                'confidence': 'low'
            }

        if positive_count > negative_count:
            raw_score = (positive_count / total) * 0.5 + 0.5
        elif negative_count > positive_count:
            raw_score = 0.5 - (negative_count / total) * 0.5
        else:
            raw_score = 0.5

        if has_negation and total > 0:
            raw_score = 1.0 - raw_score

        score = max(0.0, min(1.0, raw_score))

        if score >= 0.6:
            label = 'positive'
        elif score <= 0.4:
            label = 'negative'
        else:
            label = 'neutral'

        if total >= 5:
            confidence = 'high'
        elif total >= 2:
            confidence = 'medium'
        else:
            confidence = 'low'

        return {
            'score': round(score, 2),
            'label': label,
            'keywords_found': keywords_found[:10],
            'confidence': confidence,
            'positive_count': positive_count,
            'negative_count': negative_count
        }


class TrinethraModule:
    """Analyzes supervisor feedback transcripts using NLP techniques."""

    TOPIC_KEYWORDS = {
        'execution': ['execution', 'task', 'completion', 'delivery', 'execute', 'deliver', 'finished', 'completed', 'work'],
        'systems_building': ['system', 'process', 'framework', 'automation', 'build', 'tool', 'streamline', 'structure'],
        'kpi_impact': ['metrics', 'kpi', 'numbers', 'results', 'conversion', 'leads', 'sales', 'revenue', 'impact'],
        'change_management': ['change', 'initiative', 'innovation', 'improve', 'better', 'transform', 'new', 'different'],
        'communication': ['communication', 'feedback', 'discuss', 'collaborate', 'team', 'coordination', 'align'],
        'problem_solving': ['problem', 'issue', 'solution', 'debug', 'troubleshoot', 'challenge', 'identify'],
    }

    def analyze_feedback(self, text):
        if not text or not isinstance(text, str):
            return {
                'sentiment_score': 0.5,
                'topics': [],
                'summary': 'No feedback provided for analysis.'
            }

        sentiment_score = self._calculate_sentiment(text)
        topics = self._extract_topics(text)
        summary = self._generate_summary(text, sentiment_score)

        return {
            'sentiment_score': round(sentiment_score, 2),
            'topics': topics,
            'summary': summary
        }


    def _calculate_sentiment(self, text):
        polarity = 0.0
        if TextBlob is not None:
            try:
                polarity = TextBlob(text).sentiment.polarity
            except Exception:
                polarity = self._keyword_polarity(text)
        else:
            polarity = self._keyword_polarity(text)

        sentiment_score = (polarity + 1) / 2
        return max(0.0, min(1.0, sentiment_score))

    def _extract_topics(self, text):
        text_lower = text.lower()
        topic_scores = {}

        for topic, keywords in self.TOPIC_KEYWORDS.items():
            count = sum(text_lower.count(keyword) for keyword in keywords)
            if count > 0:
                topic_scores[topic] = count

        sorted_topics = sorted(topic_scores.items(), key=lambda x: x[1], reverse=True)
        return [topic for topic, _ in sorted_topics[:3]]

    def _generate_summary(self, text, sentiment_score):
        sentences = text.split('.')
        if not sentences:
            return "Feedback received but unable to generate summary."

        longest_sentence = max(sentences, key=len).strip()
        if not longest_sentence:
            longest_sentence = sentences[0].strip()

        if sentiment_score >= 0.7:
            sentiment_prefix = "Positive feedback:"
        elif sentiment_score <= 0.3:
            sentiment_prefix = "Critical feedback:"
        else:
            sentiment_prefix = "Mixed feedback:"

        summary = f"{sentiment_prefix} {longest_sentence[:120]}"
        if len(longest_sentence) > 120:
            summary += "..."

        return summary.strip()


def main():
    import sys

    raw_input = sys.stdin.read()
    if raw_input and raw_input.strip():
        try:
            payload = json.loads(raw_input)
            transcript = payload.get('transcript', '')
        except json.JSONDecodeError:
            sys.stdout.write(json.dumps({'error': 'Invalid JSON input'}))
            return

        result = TrinethraAssess().assess_transcript(transcript)
        sys.stdout.write(json.dumps(result))
    else:
        sample_feedback = (
            "He maintains production tracking, coordinates quality complaints, "
            "and helped optimize the machine layout. His execution is solid but hasn't yet shown systems thinking."
        )
        result = TrinethraModule().analyze_feedback(sample_feedback)
        sys.stdout.write(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
