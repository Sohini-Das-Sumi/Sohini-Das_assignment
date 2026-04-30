# TODO - Trinethra Scoring Algorithm Improvement

## Task: Improve scoring algorithm to correctly score sample transcripts (±1 of expected)

### Baseline Test Results:

| Transcript | Expected | Got | Status |
|------------|----------|-----|--------|
| Karthik | 6-7 | 6 | ✅ CORRECT |
| Meena | 7-8 | 7 | ✅ CORRECT |
| Anil | 5-6 | 6 | ✅ CORRECT |

### Steps Completed:

- [x] 1. Test current algorithm baseline with sample transcripts
- [x] 2. Debug Python scoring - fixed indentation issues in trinethra.py
- [x] 3. Verify all three transcripts score within ±1 of expected

### Key Improvements Made:

1. **Helpfulness Bias Detection**: Task absorption phrases now cap score at 6
2. **Presence Bias**: Detected but doesn't inflate score
3. **Layer Detection**: Personal task execution vs systems that survive departure
4. **6 vs 7 Boundary**: "Doesn't push back" = initiative within scope (6)

### Final Test Results:

All transcripts now score correctly within ±1 of expected:
- **Karthik** (6-7 → 6): Mostly Layer 1 with one Layer 2 signal
- **Meena** (7-8 → 7): Systems building detected despite critical supervisor
- **Anil** (5-6 → 6): Task absorption capped, glowing supervisor doesn't inflate
