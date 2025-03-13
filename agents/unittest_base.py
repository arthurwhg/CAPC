import unittest
from unittest.mock import patch
from agents.base import OpenAIChatAgent

class TestOpenAIChatAgent(unittest.TestCase):

    def setUp(self):
        # Set up a mock OpenAI API key and model for testing
        self.api_key = "mock_api_key"  # Replace with a dummy key if needed
        self.llm_model = "gpt-3.5-turbo"
        self.system_prompt = "You are a helpful assistant."
        self.agent = OpenAIChatAgent(apiKey=self.api_key, llmModel=self.llm_model, system_prompt=self.system_prompt)
        self.prompt_template = "Question: {question}"

    @patch('agents.base.ChatOpenAI')  # Mock the ChatOpenAI class
    def test_init_with_valid_params(self, MockChatOpenAI):
        # Test successful initialization with API key and model
        agent = OpenAIChatAgent(apiKey=self.api_key, llmModel=self.llm_model)
        self.assertIsNotNone(agent.chat)
        MockChatOpenAI.assert_called_once_with(temperature=0.0, model=self.llm_model, openai_api_key=self.api_key)


    def test_init_without_params(self):
        # Test initialization without API key and model
        agent = OpenAIChatAgent()
        self.assertIsNone(agent.chat)
        self.assertEqual(agent.err, "")

    def test_set_llm_model(self):
        # Test changing the LLM model
        new_model = "gpt-4"
        self.agent.setLLMModel(new_model)
        self.assertEqual(self.agent.getModel(), new_model)

    def test_get_chat(self):
        # Test getting the chat object
        self.assertIsNotNone(self.agent.getchat())

    def test_set_prompt(self):
        # Test setting a custom prompt
        self.agent.setPrompt(self.prompt_template)
        self.assertEqual(self.agent.getPrompt(), self.prompt_template)

    @patch('agents.base.ChatOpenAI')
    def test_ask_with_question(self, MockChatOpenAI):
        # Test asking a question and getting a response
        mock_chat = MockChatOpenAI.return_value
        mock_chat.return_value = {"content": "Test response"}
        question = "What is the capital of France?"
        response = self.agent.ask(question)

        self.assertEqual(response, "Test response")

    @patch('agents.base.ChatOpenAI')
    def test_ask_without_question(self, MockChatOpenAI):
        # Test asking without a question
        response = self.agent.ask()
        self.assertIsNone(response)

    def test_ask_with_error(self):
        # Simulate an error during the API call
        with patch('agents.base.ChatOpenAI') as MockChatOpenAI:
            mock_chat = MockChatOpenAI.return_value
            mock_chat.__call__.side_effect = Exception("API error")
            response = self.agent.ask("Test question")
            self.assertIsNone(response)
            self.assertTrue("API error" in self.agent.err())

    def test_ask_with_no_model(self):
        agent = OpenAIChatAgent() #no model
        response = agent.ask("Test question")
        self.assertIsNone(response)
        self.assertEqual(agent.err, "Model has not been set")

    def test_get_error(self):
        self.agent.err = "Test error"
        self.assertEqual(self.agent.err(), "Test error")

if __name__ == '__main__':
    unittest.main()
