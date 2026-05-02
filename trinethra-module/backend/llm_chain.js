const { Napi, NodeAddon } = require('node-addon-api');

const { LLMPredictor } = require('llama_index');

class LLMChainLLama22 {
  constructor(prompt, modelPath) {
    this.prompt = prompt;
    this.llmPredictor = new LLMPredictor({
      model_name: 'llama-2.2',
      model_path: modelPath,
    });
  }

  async run(inputText) {
    try {
      const response = await this.llmPredictor.predict(inputText);
      return response;
    } catch (error) {
      console.error(`Error occurred while generating response: ${error}`);
      return '';
    }
  }
}

module.exports = { LLMChainLLama22 };