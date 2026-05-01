import json
from trinethra import TrinethraAssess

# Create one instance of the advanced brain
engine = TrinethraAssess()

def process_json_batch(json_data):
    """Iterates through the 'transcripts' array to perform true batch analysis."""
    all_analyses = []
    
    # Ensure we are looking at the 'transcripts' list
    transcripts = json_data.get("transcripts", [])
    
    for entry in transcripts:
        # 1. Extract the text and names
        text = entry.get("transcript", "")
        fellow_info = entry.get("fellow", {})
        name = fellow_info.get("name", "Unknown Fellow")
        
        # 2. Use the advanced 'engine' to analyze the transcript
        # This fixes the "assess_transcript is not defined" error
        analysis = engine.assess_transcript(text)
        
        # 3. Add the metadata so the UI knows whose score this is
        analysis['fellow_name'] = name
        analysis['id'] = entry.get("id", "no-id")
        
        all_analyses.append(analysis)
            
    return all_analyses
