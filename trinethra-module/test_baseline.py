#!/usr/bin/env python
"""Test baseline with actual transcripts from transcript.json"""

import json
import os
import importlib.util

backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
trinethra_file = os.path.join(backend_dir, 'trinethra.py')

spec = importlib.util.spec_from_file_location('trinethra', trinethra_file)
trinethra = importlib.util.module_from_spec(spec)
spec.loader.exec_module(trinethra)

assessor = trinethra.TrinethraAssess()

transcript_path = os.path.join(os.path.dirname(__file__), 'transcript.json')
with open(transcript_path, 'r', encoding='utf-8') as f:
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
