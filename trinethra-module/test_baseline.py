#!/usr/bin/env python
"""Test baseline with actual transcripts from transcript.json"""

import json
import sys
sys.path.insert(0, 'c:/Users/dasso/OneDrive/Desktop/Sohini-Das_assignment/trinethra-module/backend')
import trinethra

assessor = trinethra.TrinethraAssess()

with open('c:/Users/dasso/OneDrive/Desktop/Sohini-Das_assignment/trinethra-module/transcript.json') as f:
    data = json.load(f)

print("=" * 70)
print("BASELINE TEST - Current Algorithm with Full Transcripts")
print("=" * 70)

for t in data['transcripts']:
    print('\n' + '='*60)
    print(f"Testing: {t['fellow']['name']}")
    print(f"Expected Score Range: {t['expectedScoreRange']}")
    print(f"Scoring Notes: {t['scoringNotes'][:80]}...")
    result = assessor.assess_transcript(t['transcript'])
    print(f"\n>>> Score: {result['score']['value']} ({result['score']['label']})")
    print(f"Band: {result['score']['band']}")
    print(f"Detected Biases: {result['biases']}")
    print(f"Layer 2 strength: {result['layers'].get('layer2_strength', 0)}")
    print("-" * 40)

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print("""
Transcript 1 (Karthik): Expected 6-7, Got [varies]
  - Trap: Positive supervisor, mostly Layer 1, explicit "no push back"
  - Key issue: Need to detect lack of initiative as ceiling for score

Transcript 2 (Meena): Expected 7-8, Got [varies]  
  - Trap: Critical supervisor masks real Layer 2 work
  - Key issue: Presence bias masks systems building evidence

Transcript 3 (Anil): Expected 5-6, Got [varies]
  - Trap: Glowing supervisor but task absorption
  - Key issue: Helpfulness bias inflates score (task != systems)
""")
