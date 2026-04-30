import re

# Read the backup file
with open(r'trinethra_backup.py', 'r') as f:
    content = f.read()

# Fix the indentation issue in _map_kpis function
content = content.replace(
    '        for kpi, keywords in self.KPI_KEYWORDS.items():\nif any(kw in text for kw in keywords):\n                matched_kpis.append(kpi.replace',
    '        for kpi, keywords in self.KPI_KEYWORDS.items():\n            if any(kw in text for kw in keywords):\n                matched_kpis.append(kpi.replace'
)

# Now add error handling to assess_transcript method
old_assess = '''    def assess_transcript(self, transcript):
        """
        Perform comprehensive assessment of a supervisor transcript.
        
        Args:
            transcript (str): The supervisor feedback transcript
            
        Returns:
            dict: Structured assessment with score, evidence, KPIs, gaps, questions
        """
        if not transcript or not isinstance(transcript, str):
            return {'error': 'Transcript is required'}
        
        text_lower = transcript.lower()
        
        # Extract evidence
        evidence = self._extract_evidence(transcript)
        
        # Determine layer presence
        layers = self._detect_layers(text_lower)
        
        # Map KPIs
        kpis = self._map_kpis(text_lower)
        
        # Detect assessment dimensions
        dimensions = self._detect_dimensions(text_lower)
        
        # Calculate score
        score = self._calculate_score(text_lower, evidence, layers, dimensions)
        
        # Identify gaps
        gaps = self._identify_gaps(dimensions, layers, evidence)
        
        # Generate follow-up questions
        questions = self._generate_questions(gaps, dimensions)
        
        # Detect biases
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
        }'''

new_assess = '''    def assess_transcript(self, transcript):
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
            kpis = self._map_kpis(text_lower)
        except Exception as e:
            errors.append(f"KPI mapping error: {str(e)}")
            kpis = []
        
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
            questions = self._generate_questions(gaps, dimensions)
        except Exception as e:
            errors.append(f"Question generation error: {str(e)}")
            questions = ['Has the Fellow ever come to you with a problem you had not noticed?']
        
        # Detect biases with error handling
        try:
            biases = self._detect_biases(text_lower)
        except Exception as e:
            errors.append(f"Bias detection error: {str(e)}")
            biases = []
        
        return {
            'score': score,
            'evidence': evidence,
            'kpis': kpis,
            'dimensions': dimensions,
            'gaps': gaps,
            'questions': questions,
            'biases': biases,
            'layers': layers,
            'errors': errors
        }'''

content = content.replace(old_assess, new_assess)

# Write the corrected file
with open('trinethra.py', 'w') as f:
    f.write(content)

print('File written successfully. Error handling has been applied to trinethra.py')
