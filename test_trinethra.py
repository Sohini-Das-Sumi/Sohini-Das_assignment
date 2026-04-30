from trinethra import score_transcript

sample_text = (
    "He handles all my calls and attends every meeting. "
    "He created a tracker for dispatch delays and worked with the floor team to adopt it, "
    "which reduced turnaround time."
)

result = score_transcript(sample_text)
print(result)
