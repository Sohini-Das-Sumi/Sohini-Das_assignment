#!/usr/bin/env python
"""Test script for TrinethraAssess text processing logic."""

import sys
import os
import importlib.util

backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
trinethra_file = os.path.join(backend_dir, 'trinethra.py')

spec = importlib.util.spec_from_file_location('trinethra', trinethra_file)
trinethra = importlib.util.module_from_spec(spec)
spec.loader.exec_module(trinethra)
TrinethraAssess = trinethra.TrinethraAssess
TrinethraCore = trinethra.TrinethraCore

# Create assessor
assessor = TrinethraAssess()

# Test 1: Mixed transcript with system building
test1_transcript = """
He maintains production tracking, updates the sheet every evening and sends it to me.
He built an order tracker that we now use daily.
The supervisor says he is very helpful and handles all my calls.
He doesn't really push back when I give him tasks.
"""

print("=" * 60)
print("Test 1: Karthik-style transcript (mixed Layer 1/2)")
print("=" * 60)
result1 = assessor.assess_transcript(test1_transcript)
print(f"Score: {result1['score']['value']} ({result1['score']['label']})")
print(f"Band: {result1['score']['band']}")
print(f"KPIs: {result1['kpis']}")
print(f"Dimensions: {result1['dimensions']}")
print(f"Gaps: {len(result1['gaps'])} gaps identified")
print(f"Biases: {result1['biases']}")
print()

# Test 2: Strong system builder
test2_transcript = """
She noticed our rejection rate was higher on Line 3 and quantified it.
She built a tracking system for orders and dispatch.
She created an SOP for the cutting section.
She sends a daily risk alert by 11 AM which saved a shipment last week.
"""

print("=" * 60)
print("Test 2: Meena-style transcript (strong systems building)")
print("=" * 60)
result2 = assessor.assess_transcript(test2_transcript)
print(f"Score: {result2['score']['value']} ({result2['score']['label']})")
print(f"Band: {result2['score']['band']}")
print(f"KPIs: {result2['kpis']}")
print(f"Dimensions: {result2['dimensions']}")
print(f"Gaps: {len(result2['gaps'])} gaps identified")
print(f"Biases: {result2['biases']}")
print()

# Test 3: Task absorption (high helpfulness)
test3_transcript = """
She is my right hand. I don't know how we managed before her.
She handles all my calls, runs my meetings, takes notes.
She coordinates with the distributor and manages the production schedule.
At 3 AM during the power failure she personally came to check the cold chain.
"""

print("=" * 60)
print("Test 3: Anil-style transcript (task absorption)")
print("=" * 60)
result3 = assessor.assess_transcript(test3_transcript)
print(f"Score: {result3['score']['value']} ({result3['score']['label']})")
print(f"Band: {result3['score']['band']}")
print(f"KPIs: {result3['kpis']}")
print(f"Dimensions: {result3['dimensions']}")
print(f"Gaps: {len(result3['gaps'])} gaps identified")
print(f"Biases: {result3['biases']}")
print()

# Test 4: Preprocessing still works
core = trinethra.TrinethraCore()
test4 = core.preprocess_text('He maintains production tracking, coordinates quality complaints, and helped optimize the machine layout!')
print("Test 4: Basic preprocessing (TrinethraCore)")
print("=" * 60)
print(f"Input:  'He maintains production tracking...'")
print(f"Output: '{test4}'")
print()

print("=" * 60)
print("All tests completed!")
print("=" * 60)
