const { LLMChainLLama22 } = require('./llm_chain');

const prompt = 'You are a helpful assistant. {input}.';
const modelPath = '/path/to/llama-2.2/model';
const chain = new LLMChainLLama22(prompt, modelPath);

const promptText = 'What is the weather like today?';
chain.run(promptText)
  .then(response => console.log(response))
  .catch(error => console.error(error));