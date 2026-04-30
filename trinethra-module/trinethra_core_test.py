#!/usr/bin/env python
"""Test script for TrinethraCore functionality."""

from trinethra import TrinethraCore

# Test the TrinethraCore class
core = TrinethraCore()

# Test 1: Basic preprocessing
test1 = core.preprocess_text('He maintains production tracking, coordinates quality complaints, and helped optimize the machine layout!')
print('Test 1 - Basic preprocessing:')
print('  Input:  "He maintains production tracking, coordinates quality complaints, and helped optimize the machine layout!"')
print('  Output: "' + test1 + '"')
print()

# Test 2: With special characters
test2 = core.preprocess_text('Great work @john! Your execution is solid (but needs improvement). #feedback')
print('Test 2 - Special characters:')
print('  Input:  "Great work @john! Your execution is solid (but needs improvement). #feedback"')
print('  Output: "' + test2 + '"')
print()

# Test 3: Empty input
test3 = core.preprocess_text('')
print('Test 3 - Empty input:')
print('  Output: "' + test3 + '"')
print()

# Test 4: Preserve punctuation
test4 = core.preprocess_text_preserve_punctuation('Wow! Great job?')
print('Test 4 - Preserve punctuation:')
print('  Input:  "Wow! Great job?"')
print('  Output: "' + test4 + '"')

print()
print('All tests completed successfully!')
