import unittest
from unittest.mock import patch
from assistant import Assistant
from langchain.prompts import PromptTemplate
import json
import pprint

class TestAssistant(unittest.TestCase):
  api_key = "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"
  model = "gpt-4o-mini"
  examples=[
      {"input":"list allkings in Isreal", 
      "output_jsonblob": json.dumps(
         {"king": "國王的名字，例如David","duration": "在位時長","book": "聖經書卷的名字，例如 \'耶肋米亞書\'","verse": "相關的聖經章節，例如 \'29:11\'","activity": "主要作為","end": "結局,若沒有答案，請回答未記錄"},
         ensure_ascii=False, indent=4)
      },
      {"input":"請列出以色列人離開埃及直到進入嘉南美地主要事件，發生地和大約時間，", 
       "output_jsonblob": json.dumps({
              "event": "事件",
              "place": "發生地",
              "time": "相對於出埃及的時間",
              "book": "聖經書卷的名字",
              "verse": "章節", 
              "scripture": "聖經章節",
              "activity": "主要事件",
            },ensure_ascii=False, indent=4)
      }
    ]

  # for ex in examples:
  #   print(f"Question: {ex['input']}")
  #   print("Suggested JSON Blob:")
  #   print(ex["output_jsonblob"])
  #   print("=" * 50)

  examples_template=PromptTemplate(
      input_variables=["input", "output_jsonblob"],
      template="User: {input}\nsuggested Json blob:\n{output_jsonblob}\n"
  )

  role = """"You are given some samples by input questons and output in Json blob of answers to the question.
  You are asked by a new question, please suggest your best Json blob for the response. 
  You do not need to answer the question. You just need provide 1 sample based on the Json blob you suggested
  """
  
  assistant = Assistant(apiKey=api_key, model=model, role=role, examples=examples, examples_template=examples_template)

  def test_getAssistant(self):
    #self.assistant.getAssistant("how to pray for me to seek a new job")
    print('testing Assistant feature')
    assistant = self.assistant.getAssistant("如何理解\“當將你的事交託耶和華，並倚靠他，他就必成全\”這句經文")
    pprint.pprint(json.loads(assistant))
#     @patch('agents.fewshotschatAgent.FewShowsChatAgent.getResponse') # Mock the getResponse method
#     def test_getAssistant_with_question(self, mock_getResponse):
#         # Set up mock data
#         mock_response = {"content": "This is a test response"}
#         mock_getResponse.return_value = mock_response  # Mock the response

#         # Create an instance of Assistant (replace with your actual constructor parameters)
#         api_key = "YOUR_API_KEY"  # Replace with a dummy key or remove the test if not using OpenAI
#         model = "gpt-3.5-turbo"
#         role = "Helpful assistant"  # Replace with your role description
#         examples = Assistant.examples  # Use the examples from the class
#         example_template = Assistant.examples_template
#         assistant = Assistant(api_key, model, role, examples, example_template)

#         # Call the getAssistant method with a question
#         response = assistant.getAssistant("Test question")

#         # Assert that the response is correct
#         self.assertEqual(response, "This is a test response")
#         mock_getResponse.assert_called_once() #ensure getResponse was called only once.


#     def test_getAssistant_without_question(self):
#         # Create an instance of Assistant (replace with your actual constructor parameters)
#         api_key = "YOUR_API_KEY"  # Replace with a dummy key or remove this test if not using OpenAI.
#         model = "gpt-3.5-turbo"
#         role = "Helpful assistant"
#         examples = Assistant.examples
#         example_template = Assistant.examples_template
#         assistant = Assistant(api_key, model, role, examples, example_template)

#         # Call getAssistant without a question
#         response = assistant.getAssistant()

#         # Assert that the response is None and the error message is set
#         self.assertIsNone(response)
#         self.assertEqual(assistant.err, "Please provide your question")


#     @patch('agents.fewshotschatAgent.FewShowsChatAgent.getResponse')
#     def test_getAssistant_with_error(self, mock_getResponse):
#         # Set up mock error scenario
#         mock_getResponse.side_effect = Exception("API error")

#         # Create an instance of Assistant (replace with your actual constructor parameters)
#         api_key = "YOUR_API_KEY"  # Replace with a dummy key or remove this test if not using OpenAI.
#         model = "gpt-3.5-turbo"
#         role = "Helpful assistant"
#         examples = Assistant.examples
#         example_template = Assistant.examples_template
#         assistant = Assistant(api_key, model, role, examples, example_template)

#         # Call getAssistant with a question
#         response = assistant.getAssistant("Test question")

#         # Assert that the response is None and the error message contains "API error"
#         self.assertIsNone(response)
#         self.assertIn("API error", assistant.err)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
