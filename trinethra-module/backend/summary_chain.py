import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock generateSummaryPrompt for backend (copy from frontend)
def generateSummaryPrompt(transcript):
  return f"""Generate a concise 2-3 sentence summary (50-100 words) of this supervisor feedback transcript. Focus on:
- Key strengths mentioned
- Main gaps or concerns
- Overall sentiment and performance impression

Make it editable and neutral. Output only the plain text summary, no JSON.

Transcript:
{transcript}"""

# LLM Integration - User to configure
MODEL_PATH = None  # Use Ollama mistral (local fallback works)
PROMPT_TEMPLATE = "You are a helpful assistant.\\n{summarized_prompt}"
summary_chain = None
LLM_AVAILABLE = True

try:
    from llm_chain import LLMChainLLama22
    # Initialize if needed (user configures MODEL_PATH)
    if MODEL_PATH:
        summary_chain = LLMChainLLama22(model_path=MODEL_PATH)
    print("LLM module loaded successfully (configure MODEL_PATH to enable).")
except ImportError:
    LLM_AVAILABLE = False
    print("LLM module not found - using robust fallback for summaries.")
except Exception as e:
    LLM_AVAILABLE = False
    print(f"LLM error: {e} - using robust fallback.")

def generate_summary(transcript):
    """
    Generate summary using LLM or fallback.
    """
    if LLM_AVAILABLE and summary_chain:
        try:
            full_prompt = PROMPT_TEMPLATE.format(summarized_prompt=generateSummaryPrompt(transcript))
            response = summary_chain.run(full_prompt)
            return response.strip()
        except Exception as e:
            print(f"LLM error: {e}")
    
    # Robust fallback summary: first 3 sentences
    sentences = [s.strip() for s in transcript.split('.') if s.strip()]
    fallback = '. '.join(sentences[:3]) + '.' if sentences else transcript[:300]
    return fallback[:300]

