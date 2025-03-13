import unittest
from pastor import Pastor
import json

class TestPastor(unittest.TestCase):
    api_key = "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"
    model = "gpt-4o-mini"
    pastor = Pastor(api_key, model,)

    #@patch('agents.base.ChatOpenAI')
    def test_init(self):
        print(type(self.pastor))
        print(self.pastor is not None)
        self.assertIsNotNone(self.pastor)
        #MockChatOpenAI.assert_called_once_with(temperature=0.0, model=model, openai_api_key=api_key)
        #self.assertEqual(pastor.sys_promt, """You are a christan pastor. You are asked some questions on bible or prayers.\n    Please answer customer questions and using the output format and in the language required. \n    if you were not sure about the answer, please answer I do  not know""")


    def test_printPrompts(self):
        jb ="""{
            "title": "祈禱的重點，例如 '信靠神的計劃'",
            "book": "聖經書卷的名字，例如 '耶肋米亞書'",
            "verse": "相關的聖經章節，例如 '29:11'",
            "scripture": "完整的聖經經文，提供神的應許或鼓勵，例如 '上主說：我對你們所懷的計劃，我自知，這計劃不是災禍，而是和平，令你們有前途，有希望。'",
            "prayer_point": "根據經文的祈禱內容，例如 '求神帶領我進入符合祂旨意的工作，並賜我信心相信祂的計劃是良善的。'"
            """
        #self.pastor.printPrompts("list all kings in Isreal",jb,"Chinese")

    # #@patch('agents.base.ChatOpenAI')
    # def test_get_answer_with_json_structure(self, MockChatOpenAI):
    #     #pastor = Pastor(apiKey=self.api_key, model=self.model)
    #     pastor.setOutputJsonStructure({"answer": "string"})
    #     #mock_chat = MockChatOpenAI.return_value
    #     #mock_response = {"content": '```json\n{"answer": "This is a test answer"}\n```'}
    #     #mock_chat.return_value = mock_response
    #     #response = pastor.getAnswer("Test question")
    #     #self.assertEqual(response, {"answer": "This is a test answer"})


    # @patch('agents.base.ChatOpenAI')
    # def test_get_answer_without_json_structure(self, MockChatOpenAI):
    #     pass
    #     #pastor = Pastor(apiKey=self.api_key, model=self.model)
    #     #mock_chat = MockChatOpenAI.return_value
    #     #mock_response = {"content": "This is a test answer"}
    #     #mock_chat.return_value = mock_response
    #     #response = pastor.getAnswer("Test question")
    #     #self.assertEqual(response, "This is a test answer")

    # @patch('agents.base.ChatOpenAI')
    # def test_get_answer_with_error(self, MockChatOpenAI):
    #     pastor = Pastor(apiKey=self.api_key, model=self.model)
    #     mock_chat = MockChatOpenAI.return_value
    #     mock_chat.side_effect = Exception("API error")
    #     response = pastor.getAnswer("Test question")
    #     self.assertTrue("API error" in response or "Model has not been set" in response) # handles both potential error messages

    # @patch('agents.base.ChatOpenAI')
    # def test_get_answer_no_json_in_response(self, MockChatOpenAI):
    #     #pastor = Pastor(apiKey=self.api_key, model=self.model)
    #     #pastor = Pastor(apiKey=self.api_key, model=self.model)
    #     #mock_chat = MockChatOpenAI.return_value
    #     #mock_response = {"content": "This is a test answer without json"}
    #     #mock_chat.return_value = mock_response
    #     response = self.pastor.getAnswer("please list names of all kings in Isreal")
    #     self.assertIsNone(self.pastor.error) #Should return the text as is since there is no json
    #     print(response)

    # @patch('agents.base.ChatOpenAI')
    # def test_get_answer_invalid_json(self, MockChatOpenAI):
    #     pastor = Pastor(apiKey=self.api_key, model=self.model)
    #     pastor.setOutputJsonStructure({"answer": "string"})
    #     mock_chat = MockChatOpenAI.return_value
    #     mock_response = {"content": '```json\n{"answer": "This is a test answer", "extra": }\n```'} #invalid json
    #     mock_chat.return_value = mock_response
    #     response = pastor.getAnswer("Test question")
    #     self.assertTrue("JSONDecodeError" in response or "API error" in response) # Check for error handling of invalid JSON


    # def test_set_output_json_structure(self):
    #     jb ="""{
    #         "king": "國王的名字，例如 ‘大衛’",
    #         “duration”： “在位時長”
    #         "book": "聖經書卷的名字，例如 '耶肋米亞書'",
    #         "verse": "相關的聖經章節，例如 '29:11'",
    #         "activity": "主要作為“。}
    #         "end": "結局"。若沒有答案，請回答未記錄,
    #         """
    #     answers = self.pastor.getAnswer(question="list allkings in Isreal",jsonblob=jb,
    #                     language="Chinese")
        
    #     for answer in answers:
    #         print(answer)

    def test_ask_pastor(self):
        jb ="""{
            "day": "第幾天",
            "prayer": "禱告內容",
            "book": "聖經書卷的名字，例如 '耶肋米亞書'",
            "verse": "相關的聖經章節，例如 '29:11'",
            "scripture": "經文"
            """
        answers = self.pastor.getAnswer(question='我已經失業一年了，我面試了很多次都失敗了，我該怎樣向上帝坦誠你的失落和沮喪，讓祂知道我的心情',
                                        language="Chinese")
        print(answers)
        # for answer in answers:
        #     print(answer)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
