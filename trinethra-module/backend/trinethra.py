import re
import json
import csv
from collections import Counter

try:
    from textblob import TextBlob
except ImportError:
    TextBlob = None


class TrinethraCore:
    """
    TrinethraCore provides core text preprocessing functionality for the Trinethra intelligence layer.
    
    This class handles text cleaning and normalization to prepare supervisor feedback
    for analysis by removing noise and standardizing format.
    """
    
    # Special characters to remove (configurable)
    SPECIAL_CHARACTERS = r'[^a-zA-Z0-9\s.,!?\'"-]'
    
    def preprocess_text(self, text):
        """
        Clean and normalize supervisor feedback text.
        
        Removes special characters and standardizes text to lowercase
        for consistent processing by downstream analysis components.
        
        Args:
            text (str): Raw supervisor feedback text to clean
            
        Returns:
            str: Cleaned and normalized text
        """
        if not text or not isinstance(text, str):
            return ""
        
        # Remove special characters
        cleaned = re.sub(self.SPECIAL_CHARACTERS, '', text)
        
        # Standardize to lowercase
        standardized = cleaned.lower()
        
        # Normalize whitespace (replace multiple spaces with single space)
        normalized = re.sub(r'\s+', ' ', standardized).strip()
        
        return normalized
    
    def preprocess_text_preserve_punctuation(self, text):
        """
        Clean text while preserving sentence structure punctuation.
        
        Useful when sentence boundaries need to be maintained for
        downstream analysis.
        
        Args:
            text (str): Raw supervisor feedback text to clean
            
        Returns:
            str: Cleaned text with punctuation preserved
        """
        if not text or not isinstance(text, str):
            return ""
        
        # Keep alphanumeric, common punctuation, and whitespace
        preserved_pattern = r'[^a-zA-Z0-9\s.,!?\'"-]'
        cleaned = re.sub(preserved_pattern, '', text)
        standardized = cleaned.lower()
        normalized = re.sub(r'\s+', ' ', standardized).strip()
        
        return normalized
    def process_batch(self, feedback_list):
        """Processes a list of strings and returns a summary report."""
        results = []
        total_score = 0

        for text in feedback_list:
            score = self.get_score(text) # Calls your previous logic
            results.append({"text": text, "score": score})
            total_score += score

        average = total_score / len(feedback_list) if feedback_list else 0
        
        return {
            "average_team_score": round(average, 2),
            "total_entries": len(feedback_list),
            "detailed_results": results
        }

    def process_csv(self, file_path):
        """Reads a CSV, extracts the feedback column, and processes it."""
        feedbacks = []
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Assuming your CSV column is named 'feedback'
                feedbacks.append(row['feedback'])
        
        return self.process_batch(feedbacks)
    
    def __init__(self):
        # Basic scoring dictionary for logic
        self.sentiment_map = {
            "excellent": 10, "great": 9, "good": 8, 
            "progress": 7, "inconsistent": 4, "struggles": 2
        }

    def preprocess_text(self, text):
        """Cleans the text: lowercase and removes special characters."""
        text = text.lower()
        return re.sub(r'[^a-zA-Z0-9\s]', '', text)

    def get_score(self, text):
        """Simple scoring logic based on keyword detection."""
        clean_text = self.preprocess_text(text)
        score = 5  # Default neutral score
        for word, value in self.sentiment_map.items():
            if word in clean_text:
                score = value
        return score

    def process_batch(self, feedback_list):
        """Processes a list of strings and returns a summary report."""
        results = []
        total_score = 0

        for text in feedback_list:
            score = self.get_score(text)
            results.append({"text": text, "score": score})
            total_score += score

        average = total_score / len(feedback_list) if feedback_list else 0
        
        return {
            "average_team_score": round(average, 2),
            "total_entries": len(feedback_list),
            "detailed_results": results
        }

    def process_csv(self, file_path):
        """Reads a CSV, extracts the feedback column, and processes it."""
        feedbacks = []
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # We use the column name 'feedback' from our test CSV
                    feedbacks.append(row['feedback'])
            
            return self.process_batch(feedbacks)
        except FileNotFoundError:
            return {"error": "File not found. Please check the file path."}
        except KeyError:
            return {"error": "Column 'feedback' not found in CSV."}

# --- TEST RUNNER SECTION ---
if __name__ == "__main__":
    analyzer = TrinethraCore()
    
    # Ensure 'test_feedback.csv' exists in the same folder
    report = analyzer.process_csv('test_feedback.csv')
    
    if "error" in report:
        print(f"Error: {report['error']}")
    else:
        print("-" * 30)
        print("TRINETHRA BATCH REPORT")
        print("-" * 30)
        print(f"Total Entries: {report['total_entries']}")
        print(f"Team Performance Average: {report['average_team_score']}/10")
        print("-" * 30)


class TrinethraAssess:
    """
    TrinethraAssess provides structured assessment logic for DT Fellow performance evaluation.
    
    Implements Layer detection (Execution vs Systems Building), KPI mapping, 
    rubric-based scoring, dimension detection, and bias identification.
    """
    
    # Sentiment keywords for supervisor feedback analysis
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
    
    # Neutral/modifier keywords that adjust sentiment
    NEUTRAL_KEYWORDS = [
        'okay', 'alright', 'fine', 'average', 'normal', 'standard', 'typical', 'usual',
        'basic', 'simple', 'moderate', 'decent', 'adequate', 'acceptable'
    ]
    
    # Intensifiers (increase sentiment strength)
    INTENSIFIERS = ['very', 'really', 'extremely', 'absolutely', 'totally', 'completely', 'highly']
    
    # Negators (flip sentiment)
    NEGATORS = ['not', "n't", 'never', 'no', 'hardly', 'barely', 'rarely']
    
    # KPI keywords mapping (supervisor plain language -> KPI categories)
    KPI_KEYWORDS = {
        'lead_generation': ['new customers', 'new schools', 'leads', 'potential clients', 'prospects', 'find new', 'identify', 'contact'],
        'lead_conversion': ['closed', 'converted', 'new account', 'signed', 'paid', 'became a customer', 'won'],
        'upselling': ['bigger', 'more', 'increased', 'bigger order', 'grew', 'selling more'],
        'cross_selling': ['additional', 'along with', 'also started', 'extra', '包装', 'packaging along'],
        'nps': ['happy', 'satisfied', 'happier', 'recommend', 'fewer complaints', 'satisfaction', 'pleased', 'no complaints'],
        'pat': ['waste', 'reduced', 'costs came', 'saved', 'profit', 'margin', 'inefficient', 'cheaper'],
        'tat': ['faster', 'dispatch', 'quicker', 'turnaround', 'speed', 'deadline', 'on time', 'timely'],
        'quality': ['rejection', 'defect', 'complaint', 'quality', 'reject', 'error', 'issue', 'problem']
    }
    
    # Layer detection keywords
    LAYER_1_KEYWORDS = ['helps', 'maintains', 'updates', 'handles', 'coordinates', 'assists', 'does', 'takes', 'runs', 'manages']
    LAYER_2_KEYWORDS = ['built', 'created', 'designed', 'started', 'set up', 'developed', 'automated', 'streamlined', 'documented', 'implemented']
    
    # Assessment dimension keywords
    DIMENSION_KEYWORDS = {
'Driving Execution': ['task', 'delivers', 'on time', 'follow up', 'initiates', 'completes', 'finishes', 'gets done', 'starts working'],
        'Building Systems': ['system', 'tracker', 'sheet', 'template', 'process', 'automate', 'structure', ' SOP', 'document'],
        'KPI Impact': ['faster', 'saved', 'reduced', 'increased', 'improved', 'dropped', 'better', 'numbers', 'metrics'],
        'Change Management': ['resistance', 'adopt', 'workers', 'floor team', 'introduce', 'new process', 'compliance', 'listen to']
    }

    # Supervisor bias indicators
    BIAS_INDICATORS = {
        'helpfulness': ['handles all', 'takes off my plate', 'big relief', 'helper', 'does everything', 'relieves', 'my right hand', "don't know how we managed"],
        'presence': ['always on', 'on the floor', 'physically', 'present', 'never leaves'],
        'halo': ['love', 'glowing', 'amazing', 'fantastic', 'couldn\'t manage without'],
        'recency': ['last week', 'recently', 'lately', 'these days', 'past few']
    }
    
    # Task absorption phrases - indicate personal dependency, NOT systems building
    TASK_ABSORPTION_PHRASES = [
        'runs my', 'takes my calls', 'handles all my', 'coordinates with',
        'manages my', 'does my', 'in my office', 'personal',
        'takes so much off', 'takes over', 'does another', 'doing raghav\'s'
    ]
    
    # Rubric band definitions
    RUBRIC_BANDS = {
        'Need Attention': {'range': [1, 3], 'levels': [1, 2, 3]},
        'Productivity': {'range': [4, 6], 'levels': [4, 5, 6]},
        'Performance': {'range': [7, 10], 'levels': [7, 8, 9, 10]}
    }
    
    def assess_transcript(self, transcript):
        """
        Perform comprehensive assessment of a supervisor transcript.
        
        Args:
            transcript (str): The supervisor feedback transcript
            
        Returns:
            dict: Structured assessment with score, evidence, KPIs, gaps, questions
        """
        errors = []
        
        if not transcript or not isinstance(transcript, str):
            return {'error': 'Transcript is required', 'errors': ['Transcript is required']}
        
        text_lower = transcript.lower()
        
        # Extract evidence with error handling
        try:
            evidence = self._extract_evidence(transcript)
        except Exception as e:
            errors.append(f"Evidence extraction error: {str(e)}")
            evidence = []
        
        # Determine layer presence with error handling
        try:
            layers = self._detect_layers(text_lower)
        except Exception as e:
            errors.append(f"Layer detection error: {str(e)}")
            layers = {'execution': True, 'systems_building': False, 'layer2_strength': 0}
        
        # Map KPIs with error handling
        try:
            kpi_mapping = self._map_kpis_detailed(text_lower)
        except Exception as e:
            errors.append(f"KPI mapping error: {str(e)}")
            kpi_mapping = []
        
        # Detect assessment dimensions with error handling
        try:
            dimensions = self._detect_dimensions(text_lower)
        except Exception as e:
            errors.append(f"Dimension detection error: {str(e)}")
            dimensions = {'Driving Execution': True, 'Building Systems': False, 'KPI Impact': False, 'Change Management': False}
        
        # Calculate score with error handling
        try:
            score = self._calculate_score(text_lower, evidence, layers, dimensions)
        except Exception as e:
            errors.append(f"Score calculation error: {str(e)}")
            score = {
                'value': 5,
                'label': 'Consistent Performer',
                'band': 'Productivity',
                'justification': 'Assessment encountered errors. Default score applied.'
            }
        
        # Identify gaps with error handling
        try:
            gaps = self._identify_gaps(dimensions, layers, evidence)
        except Exception as e:
            errors.append(f"Gap identification error: {str(e)}")
            gaps = []
        
        # Generate follow-up questions with error handling
        try:
            follow_up_questions = self._generate_follow_up_questions(gaps, dimensions)
        except Exception as e:
            errors.append(f"Question generation error: {str(e)}")
            follow_up_questions = [{'question': 'Has the Fellow ever come to you with a problem you had not noticed?', 'targetGap': 'problem_identification', 'lookingFor': 'Evidence of independent problem identification.'}]
        
        # Detect biases with error handling
        try:
            biases = self._detect_biases(text_lower)
        except Exception as e:
            errors.append(f"Bias detection error: {str(e)}")
            biases = []
        
        return {
            'score': score,
            'evidence': evidence,
            'kpiMapping': kpi_mapping,
            'gaps': gaps,
            'followUpQuestions': follow_up_questions,
            'errors': errors
        }
    
    def _extract_evidence(self, transcript):
        """Extract evidence quotes from transcript."""
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
        """Classify a sentence to an assessment dimension."""
        scores = {}
        
        for dim, keywords in self.DIMENSION_KEYWORDS.items():
            count = sum(1 for kw in keywords if kw in text)
            scores[dim] = count
        
        if not scores or max(scores.values()) == 0:
            return 'Driving Execution'
        
        return max(scores, key=scores.get)
    
    def _detect_layers(self, text):
        """Detect Layer 1 (Execution) vs Layer 2 (Systems Building) presence."""
        layer1_score = sum(1 for kw in self.LAYER_1_KEYWORDS if kw in text)
        layer2_score = sum(1 for kw in self.LAYER_2_KEYWORDS if kw in text)
        
        return {
            'execution': layer1_score > layer2_score,
            'systems_building': layer2_score >= layer1_score,
            'layer2_strength': layer2_score
        }
    
    def _map_kpis_detailed(self, text):
        """Map transcript text to KPI categories with evidence and system/personal classification."""
        kpi_mappings = []
        
        for kpi, keywords in self.KPI_KEYWORDS.items():
            if any(kw in text for kw in keywords):
                # Find evidence quote
                evidence_quote = self._find_kpi_evidence(text, keywords)
                
                # Determine if system or personal
                system_or_personal = 'personal'  # default
                if any(sys_word in text.lower() for sys_word in ['built', 'created', 'tracker', 'process', 'system']):
                    system_or_personal = 'system'
                
                kpi_mappings.append({
                    'kpi': kpi.replace('_', ' ').title(),
                    'evidence': evidence_quote,
                    'systemOrPersonal': system_or_personal
                })
        
        return kpi_mappings[:4]
    
    def _find_kpi_evidence(self, text, keywords):
        """Find a relevant quote for KPI evidence."""
        sentences = re.split(r'[.!?]+', text)
        for sentence in sentences:
            if any(kw in sentence.lower() for kw in keywords):
                return sentence.strip()[:150]
        return "KPI impact mentioned in transcript."
    
    def _detect_dimensions(self, text):
        """Detect which assessment dimensions are covered."""
        dimensions = {}
        
        for dim, keywords in self.DIMENSION_KEYWORDS.items():
            present = any(kw in text for kw in keywords)
            dimensions[dim] = present
        
        return dimensions
    
    def _sentence_polarity(self, sentence):
        """Return polarity score for a sentence, using TextBlob if available."""
        if TextBlob is not None:
            try:
                return TextBlob(sentence).sentiment.polarity
            except Exception:
                pass
        return self._keyword_polarity(sentence)

    def _keyword_polarity(self, text):
        """Fallback sentiment polarity using keyword counts."""
        text_lower = text.lower()
        positive_count = sum(1 for kw in self.POSITIVE_KEYWORDS if kw in text_lower)
        negative_count = sum(1 for kw in self.NEGATIVE_KEYWORDS if kw in text_lower)
        total = positive_count + negative_count
        if total == 0:
            return 0.0
        return (positive_count - negative_count) / total

    def _calculate_score(self, text, evidence, layers, dimensions):
        """Calculate rubric score based on evidence and patterns."""
        
        # Detect task absorption (personal dependency) - caps score at 6
        has_task_absorption = any(phrase in text for phrase in self.TASK_ABSORPTION_PHRASES)
        
        # Check for problem identification (Level 7+ signal)
        problem_identifier_phrases = ['noticed', 'found that', 'discovered', 'identified', 'quantified', 'tracked', 'analysis']
        has_problem_id = any(phrase in text for phrase in problem_identifier_phrases)
        
        # Check for system creation (Layer 2 strong)
        has_system_creation = layers['systems_building'] and layers['layer2_strength'] >= 2
        
        # Check for lack of initiative (negative signal - ceiling at 6)
        lack_initiative = ['doesn\'t push back', 'doesn\'t question', 'just does', 'no initiative', 'does what i tell', 'tells him to do']
        has_lack_initiative = any(phrase in text for phrase in lack_initiative)
        
        # Dimension coverage
        dimension_count = sum(dimensions.values())
        
        # Base core score calculation (before bias adjustments)
        if has_lack_initiative:
            core_score = 5  # Ceiling at 5-6 due to no initiative
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
        
        # Apply bias caps
        # Task absorption caps at 6 (if Fellow personally runs things)
        if has_task_absorption and core_score > 6:
            core_score = 6
        
        # If no initiative (lack of push back), cap at 6
        if has_lack_initiative and core_score > 6:
            core_score = 6
        
        base_score = core_score
        
        # Get band and label
        if base_score <= 3:
            band = 'Need Attention'
            label = 'Motivated but Directionless' if base_score == 3 else 'Consistent Performer'
        elif base_score <= 6:
            band = 'Productivity'
            labels = {4: 'Careless and Inconsistent', 5: 'Consistent Performer', 6: 'Reliable and Productive'}
            label = labels.get(base_score, 'Consistent Performer')
        else:
            band = 'Performance'
            labels = {7: 'Problem Identifier', 8: 'Problem Solver', 9: 'Innovative and Experimental', 10: 'Exceptional Performer'}
            label = labels.get(base_score, 'Problem Identifier')
        
        justification = self._generate_justification(base_score, text, layers, dimensions)
        
        return {
            'value': base_score,
            'label': label,
            'band': band,
            'justification': justification
        }
    
    def _generate_justification(self, score, text, layers, dimensions):
        """Generate justification for the score."""
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
        """Identify gaps in the transcript coverage."""
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
    
    def _generate_follow_up_questions(self, gaps, dimensions):
        """Generate follow-up questions based on gaps."""
        questions = []
        
        for gap in gaps:
            dim = gap['dimension']
            
            if dim == 'systems_building':
                questions.append({
                    'question': 'If the Fellow took a week off, what would stop working? What would keep running on its own?',
                    'targetGap': 'systems_building',
                    'lookingFor': 'Evidence of self-sustaining systems vs. personal task execution.'
                })
            elif dim == 'change_management':
                questions.append({
                    'question': 'How do the floor workers respond when the Fellow asks them to do something differently?',
                    'targetGap': 'change_management',
                    'lookingFor': 'Whether the Fellow can influence experienced workers to adopt new processes.'
                })
            elif dim == 'kpi_impact':
                questions.append({
                    'question': 'Since the Fellow started, has any specific number improved — speed, complaints, rejections?',
                    'targetGap': 'kpi_impact',
                    'lookingFor': 'Quantifiable business outcomes from the Fellow\'s work.'
                })
            elif dim == 'building_systems':
                questions.append({
                    'question': 'Has the Fellow built anything that your team uses regularly after they leave?',
                    'targetGap': 'building_systems',
                    'lookingFor': 'Systems or tools that survive the Fellow\'s departure.'
                })
            elif dim == 'execution':
                questions.append({
                    'question': 'Has the Fellow ever come to you with a problem you hadn\'t noticed?',
                    'targetGap': 'problem_identification',
                    'lookingFor': 'Evidence of independent problem identification beyond assigned tasks.'
                })
        
        # Add general questions if needed
        if len(questions) < 3:
            questions.append({
                'question': 'When was the last time the Fellow suggested a new approach or process?',
                'targetGap': 'initiative',
                'lookingFor': 'Recent examples of independent thinking or process improvement.'
            })
        
        return questions[:3]
    
    def _detect_biases(self, text):
        """Detect potential supervisor biases."""
        detected_biases = []
        
        for bias, indicators in self.BIAS_INDICATORS.items():
            if any(ind in text for ind in indicators):
                detected_biases.append(bias)
        
        return detected_biases
    
    def analyze_sentiment_keywords(self, text):
        """
        Analyze sentiment using keyword-based approach (supplements TextBlob).
        
        Returns a dict with:
        - score: 0-1 scale (0=negative, 0.5=neutral, 1=positive)
        - label: 'positive', 'negative', or 'neutral'
        - keywords_found: list of matched sentiment keywords with their type
        - confidence: 'high', 'medium', or 'low' based on keyword density
        """
        text_lower = text.lower()
        
        # Count positive and negative keywords
        positive_count = sum(1 for kw in self.POSITIVE_KEYWORDS if kw in text_lower)
        negative_count = sum(1 for kw in self.NEGATIVE_KEYWORDS if kw in text_lower)
        
        # Track which specific keywords were found
        keywords_found = []
        
        for kw in self.POSITIVE_KEYWORDS:
            if kw in text_lower:
                keywords_found.append({'keyword': kw, 'type': 'positive'})
        
        for kw in self.NEGATIVE_KEYWORDS:
            if kw in text_lower:
                keywords_found.append({'keyword': kw, 'type': 'negative'})
        
        # Handle negators (flip sentiment of following word)
        # This is a simplified approach - in production would use dependency parsing
        has_negation = any(neg in text_lower for neg in self.NEGATORS)
        
        # Calculate base score
        total = positive_count + negative_count
        
        if total == 0:
            return {
                'score': 0.5,
                'label': 'neutral',
                'keywords_found': [],
                'confidence': 'low'
            }
        
        # Calculate ratio-based score
        if positive_count > negative_count:
            raw_score = (positive_count / total) * 0.5 + 0.5  # 0.5 to 1.0
        elif negative_count > positive_count:
            raw_score = 0.5 - (negative_count / total) * 0.5  # 0.0 to 0.5
        else:
            raw_score = 0.5  # Equal = neutral
        
        # Apply negation flip
        if has_negation and total > 0:
            raw_score = 1.0 - raw_score  # Flip the score
        
        # Clip to 0-1 range
        score = max(0.0, min(1.0, raw_score))
        
        # Determine label
        if score >= 0.6:
            label = 'positive'
        elif score <= 0.4:
            label = 'negative'
        else:
            label = 'neutral'
        
        # Confidence based on keyword density
        if total >= 5:
            confidence = 'high'
        elif total >= 2:
            confidence = 'medium'
        else:
            confidence = 'low'
        
        return {
            'score': round(score, 2),
            'label': label,
            'keywords_found': keywords_found[:10],  # Limit to top 10
            'confidence': confidence,
            'positive_count': positive_count,
            'negative_count': negative_count
        }


class TrinethraBatchProcessor:
    """
    TrinethraBatchProcessor handles batch processing of multiple feedback transcripts.
    
    Provides functionality to process lists of feedbacks or CSV files and generate
    comprehensive summary reports with aggregated statistics.
    """

    def __init__(self):
        self.assessor = TrinethraAssess()

    def process_batch_feedbacks(self, feedback_list):
        """
        Process a list of feedback transcripts and return a comprehensive summary report.

        Args:
            feedback_list (list): List of feedback transcript strings

        Returns:
            dict: Comprehensive batch processing report
        """
        if not feedback_list or not isinstance(feedback_list, list):
            return {'error': 'Feedback list must be a non-empty list of strings'}

        results = []
        errors = []
        total_scores = []
        band_counts = {'Need Attention': 0, 'Productivity': 0, 'Performance': 0}
        kpi_counts = {}
        gap_counts = {}
        layer_stats = {'execution_only': 0, 'systems_building': 0, 'mixed': 0}

        for i, feedback in enumerate(feedback_list):
            try:
                if not isinstance(feedback, str) or not feedback.strip():
                    errors.append(f'Entry {i+1}: Invalid or empty feedback')
                    continue

                assessment = self.assessor.assess_transcript(feedback.strip())

                if 'error' in assessment:
                    errors.append(f'Entry {i+1}: {assessment["error"]}')
                    continue

                # Extract key metrics
                score_value = assessment['score']['value']
                band = assessment['score']['band']

                total_scores.append(score_value)
                band_counts[band] += 1

                # Count KPIs
                for kpi in assessment.get('kpiMapping', []):
                    kpi_name = kpi.get('kpi', 'Unknown')
                    kpi_counts[kpi_name] = kpi_counts.get(kpi_name, 0) + 1

                # Count gaps
                for gap in assessment.get('gaps', []):
                    gap_type = gap.get('dimension', 'unknown')
                    gap_counts[gap_type] = gap_counts.get(gap_type, 0) + 1

                # Layer statistics
                layers = assessment.get('layers', {})
                if layers.get('systems_building') and layers.get('execution'):
                    layer_stats['mixed'] += 1
                elif layers.get('systems_building'):
                    layer_stats['systems_building'] += 1
                else:
                    layer_stats['execution_only'] += 1

                # Store individual result
                results.append({
                    'index': i + 1,
                    'score': score_value,
                    'band': band,
                    'label': assessment['score']['label'],
                    'kpis': [k['kpi'] for k in assessment.get('kpiMapping', [])],
                    'gaps': [g['dimension'] for g in assessment.get('gaps', [])],
                    'layers': layers,
                    'errors': assessment.get('errors', [])
                })

            except Exception as e:
                errors.append(f'Entry {i+1}: Unexpected error - {str(e)}')

        # Calculate summary statistics
        summary = self._generate_batch_summary(total_scores, band_counts, kpi_counts, gap_counts, layer_stats, len(feedback_list), errors)

        return {
            'summary': summary,
            'results': results,
            'errors': errors,
            'total_processed': len(results),
            'total_errors': len(errors)
        }

    def process_csv_file(self, file_path, feedback_column='feedback'):
        """
        Process feedback transcripts from a CSV file.

        Args:
            file_path (str): Path to the CSV file
            feedback_column (str): Name of the column containing feedback text

        Returns:
            dict: Batch processing report
        """
        try:
            import csv
        except ImportError:
            return {'error': 'CSV processing requires the csv module'}

        feedback_list = []

        try:
            with open(file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)

                # Check if the specified column exists
                if feedback_column not in reader.fieldnames:
                    available_columns = ', '.join(reader.fieldnames)
                    return {
                        'error': f'Column "{feedback_column}" not found in CSV. Available columns: {available_columns}'
                    }

                for row_num, row in enumerate(reader, 1):
                    feedback = row.get(feedback_column, '').strip()
                    if feedback:
                        feedback_list.append(feedback)
                    else:
                        # Keep track of empty entries but don't add them
                        pass

        except FileNotFoundError:
            return {'error': f'CSV file not found: {file_path}'}
        except Exception as e:
            return {'error': f'Error reading CSV file: {str(e)}'}

        if not feedback_list:
            return {'error': f'No valid feedback found in column "{feedback_column}"'}

        return self.process_batch_feedbacks(feedback_list)

    def _generate_batch_summary(self, scores, band_counts, kpi_counts, gap_counts, layer_stats, total_entries, errors):
        """
        Generate comprehensive summary statistics for the batch.
        """
        if not scores:
            return {
                'total_entries': total_entries,
                'processed_entries': 0,
                'average_score': 0,
                'score_distribution': {},
                'band_distribution': band_counts,
                'common_kpis': {},
                'common_gaps': {},
                'layer_distribution': layer_stats,
                'error_rate': 100.0 if total_entries > 0 else 0
            }

        # Calculate score statistics
        avg_score = sum(scores) / len(scores)
        min_score = min(scores)
        max_score = max(scores)

        # Score distribution
        score_ranges = {'1-3': 0, '4-6': 0, '7-10': 0}
        for score in scores:
            if score <= 3:
                score_ranges['1-3'] += 1
            elif score <= 6:
                score_ranges['4-6'] += 1
            else:
                score_ranges['7-10'] += 1

        # Sort KPIs and gaps by frequency
        top_kpis = sorted(kpi_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        top_gaps = sorted(gap_counts.items(), key=lambda x: x[1], reverse=True)[:5]

        return {
            'total_entries': total_entries,
            'processed_entries': len(scores),
            'average_score': round(avg_score, 2),
            'min_score': min_score,
            'max_score': max_score,
            'score_distribution': score_ranges,
            'band_distribution': band_counts,
            'common_kpis': dict(top_kpis),
            'common_gaps': dict(top_gaps),
            'layer_distribution': layer_stats,
            'error_rate': round((len(errors) / total_entries) * 100, 2) if total_entries > 0 else 0
        }


class TrinethraModule:
    """
    TrinethraModule analyzes supervisor feedback transcripts using NLP techniques.
    """
    
    # Common topics to detect in feedback
    TOPIC_KEYWORDS = {
        'execution': ['execution', 'task', 'completion', 'delivery', 'execute', 'deliver', 'finished', 'completed', 'work'],
        'systems_building': ['system', 'process', 'framework', 'automation', 'build', 'tool', 'streamline', 'structure'],
        'kpi_impact': ['metrics', 'kpi', 'numbers', 'results', 'conversion', 'leads', 'sales', 'revenue', 'impact'],
        'change_management': ['change', 'initiative', 'innovation', 'improve', 'better', 'transform', 'new', 'different'],
        'communication': ['communication', 'feedback', 'discuss', 'collaborate', 'team', 'coordination', 'align'],
        'problem_solving': ['problem', 'issue', 'solution', 'debug', 'troubleshoot', 'challenge', 'identify'],
    }
    
    def analyze_feedback(self, text):
        """
        Analyze supervisor feedback and return structured insights.
        
        Args:
            text (str): The feedback transcript to analyze
            
        Returns:
            dict: Contains sentiment_score (0-1), topics (list), and summary (str)
        """
        if not text or not isinstance(text, str):
            return {
                'sentiment_score': 0.5,
                'topics': [],
                'summary': 'No feedback provided for analysis.'
            }
        
        # Calculate sentiment score
        sentiment_score = self._calculate_sentiment(text)
        
        # Extract primary topics
        topics = self._extract_topics(text)
        
        # Generate one-sentence summary
        summary = self._generate_summary(text, sentiment_score)
        
        return {
            'sentiment_score': round(sentiment_score, 2),
            'topics': topics,
            'summary': summary
        }
    
    def _calculate_sentiment(self, text):
        """
        Calculate sentiment score using TextBlob if available, otherwise fallback to keyword-based scoring.
        Converts to a 0-1 scale for compatibility with the output format.
        """
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
        """
        Extract primary topics from feedback based on keyword matching.
        Returns top 3 topics most frequently mentioned.
        """
        text_lower = text.lower()
        topic_scores = {}
        
        for topic, keywords in self.TOPIC_KEYWORDS.items():
            count = sum(text_lower.count(keyword) for keyword in keywords)
            if count > 0:
                topic_scores[topic] = count
        
        # Sort by frequency and return top 3
        sorted_topics = sorted(topic_scores.items(), key=lambda x: x[1], reverse=True)
        return [topic for topic, _ in sorted_topics[:3]]
    
    def _generate_summary(self, text, sentiment_score):
        """
        Generate a one-sentence summary of the feedback.
        """
        # Extract key metrics/adjectives from text
        sentences = text.split('.')
        if not sentences:
            return "Feedback received but unable to generate summary."
        
        # Use the longest/most substantive sentence as base
        longest_sentence = max(sentences, key=len).strip()
        
        if not longest_sentence:
            longest_sentence = sentences[0].strip()
        
        # Create sentiment-aware summary
        if sentiment_score >= 0.7:
            sentiment_prefix = "Positive feedback:"
        elif sentiment_score <= 0.3:
            sentiment_prefix = "Critical feedback:"
        else:
            sentiment_prefix = "Mixed feedback:"
        
        # Limit to ~150 characters
        summary = f"{sentiment_prefix} {longest_sentence[:120]}"
        if len(longest_sentence) > 120:
            summary += "..."
        
        return summary.strip()


if __name__ == "__main__":
    # Example 1: Batch processing with a list of feedbacks
    batch_processor = TrinethraBatchProcessor()
    
    test_feedbacks = [
        "He is very reliable and gets things done on time. Always follows instructions perfectly.",
        "She built an excellent tracking system for production and identified key bottlenecks. Team uses her tools daily.",
        "He does what I ask but doesn't take initiative. No systems thinking evident.",
        "She noticed quality issues and created a dashboard that reduced defects by 20%. Outstanding work.",
        "He helps with coordination but everything stops when he's not there. No lasting systems."
    ]
    
    print("\n" + "="*60)
    print("BATCH PROCESSING EXAMPLE 1: Feedback List")
    print("="*60)
    
    batch_result = batch_processor.process_batch_feedbacks(test_feedbacks)
    
    if 'error' in batch_result:
        print(f"Error: {batch_result['error']}")
    else:
        summary = batch_result['summary']
        print(f"\nSummary Statistics:")
        print(f"  Total entries: {summary['total_entries']}")
        print(f"  Processed: {summary['processed_entries']}")
        print(f"  Average score: {summary['average_score']}/10")
        print(f"  Min score: {summary['min_score']}, Max score: {summary['max_score']}")
        print(f"\nScore Distribution (1-3: Need Attention, 4-6: Productivity, 7-10: Performance):")
        print(f"  {summary['score_distribution']}")
        print(f"\nBand Distribution:")
        for band, count in summary['band_distribution'].items():
            print(f"  {band}: {count} Fellows")
        print(f"\nTop KPIs (Most Common):")
        for kpi, count in summary['common_kpis'].items():
            print(f"  {kpi}: {count} mentions")
        print(f"\nMost Common Gaps:")
        for gap, count in summary['common_gaps'].items():
            print(f"  {gap}: {count} instances")
        print(f"\nLayer Distribution:")
        print(f"  Execution only: {summary['layer_distribution']['execution_only']}")
        print(f"  Systems building: {summary['layer_distribution']['systems_building']}")
        print(f"  Mixed: {summary['layer_distribution']['mixed']}")
        print(f"\nError rate: {summary['error_rate']}%")
        
        print(f"\n{'='*60}")
        print("Individual Results Summary:")
        print(f"{'='*60}")
        for result in batch_result['results']:
            print(f"Entry {result['index']}: Score {result['score']} - {result['label']} ({result['band']})")
            if result['kpis']:
                print(f"  KPIs: {', '.join(result['kpis'])}")
            if result['errors']:
                print(f"  Errors: {', '.join(result['errors'])}")
    
    # Example 2: CSV file processing (if a test CSV exists)
    print(f"\n{'='*60}")
    print("BATCH PROCESSING EXAMPLE 2: CSV File (Optional)")
    print(f"{'='*60}")
    
    import os
    if os.path.exists('test_feedbacks.csv'):
        print("\nProcessing CSV file: test_feedbacks.csv")
        csv_result = batch_processor.process_csv_file('test_feedbacks.csv', feedback_column='feedback')
        
        if 'error' in csv_result:
            print(f"Error: {csv_result['error']}")
        else:
            csv_summary = csv_result['summary']
            print(f"CSV Results: {csv_summary['processed_entries']} feedbacks processed")
            print(f"Average score: {csv_summary['average_score']}")
    else:
        print("\nNo test_feedbacks.csv found. To test CSV processing:")
        print("1. Create a CSV file with columns: 'feedback', 'fellow_name' (optional)")
        print("2. Run: batch_processor.process_csv_file('your_file.csv')")


