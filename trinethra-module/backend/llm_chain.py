from llama_index import LLMPredictor, SimpleDirectoryReader, LLMApiError
from llama_index.llms import LLMChain

class LLMChainLLama22(LLMChain):
    def __init__(self, prompt: str, model_path: str):
        super().__init__(prompt)
        self.llm_predictor = LLMPredictor(
            model_name="openai/llama-2.2",
            model_path=model_path
        )

    def run(self, input_text: str) -> str:
        try:
            response = self.llm_predictor.predict(input_text)
            return response
        except LLMApiError as e:
            print(f"Error occurred while generating response: {e}")
            return ""

# Example usage
prompt = "You are a helpful assistant. {input}."
model_path = "/path/to/llama-2.2/model"
chain = LLMChainLLama22(prompt, model_path)
prompt_text = "What is the weather like today?"
response = chain.run(prompt_text)
print(response)