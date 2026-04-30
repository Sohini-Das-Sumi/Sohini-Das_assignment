# TODO: Text Processing Logic Implementation

## Task: Add text processing logic for Trinethra based on DeepThought reference material

### Information Gathered from File Analysis:
- Current `backend/trinethra.py` has basic preprocessing only
- `rubric.json` contains full 1-10 rubric with bands, levels, critical boundary
- `transcript.json` contains 3 sample transcripts with expected score ranges
- Reference material defines: Two Layers (Execution vs Systems Building), 8 KPIs, 4 Assessment Dimensions, Supervisor Biases

### Implementation Steps:

1. [X] **Create Enhanced TrinethraAssess Class** in `trinethra-module/backend/trinethra.py`
   - Add class with Layer detection logic (Execution vs Systems Building patterns)
   - Implement KPI keyword mapping (supervisor phrases → 8 KPIs)
   - Add structured rubric scoring with evidence extraction
   - Implement 4 dimension detection (Driving Execution, Systems Building, KPI Impact, Change Management)
   - Add bias detection heuristics (helpfulness, presence, halo/horn, recency)

2. [X] **Add Signal Dictionaries**
   - Layer signals: execution_keywords vs systems_building_keywords
   - KPI signals: keyword → 8 KPIs mapping
   - Dimension signals: phrases mapped to each dimension
   - Bias indicators: phrases indicating supervisor biases

3. [X] **Implement Structured Scoring Logic**
   - Score boundary detection (6 vs 7 critical boundary)
   - Evidence extraction tied to rubric levels
   - Gap analysis for missing dimensions

4. [X] **Update Test Script** to verify new functionality works

5. [X] **Follow-up**: Test with sample transcripts to validate accuracy

### Test Results:
- Test 1 (Karthik): Score 6 - correctly identifies helpfulness bias ✓
- Test 2 (Meena): Score 8 - correctly identifies systems building ✓  
- Test 3 (Anil): Score 5 - correctly identifies task absorption and bias ✓
- Test 4: Preprocessing still works ✓
