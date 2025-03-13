from fewshotschatAgent import FewShotsChatAgent
from langchain.prompts import FewShotPromptTemplate, PromptTemplate
import json

class Assistant(FewShotsChatAgent):

  def __init__(self, apiKey, model, role, examples, examples_template):
    super().__init__(apiKey, model, role, examples, examples_template)
    self.role = role
    self.examples=[
        {"input":"list allkings in Isreal", 
         "output_jsonblob": """'''json
           {"king": "國王的名字，例如David",
            "duration": "在位時長",
            "book": "聖經書卷的名字，例如 \"耶肋米亞書\"",
            "verse": "相關的聖經章節，例如 \"29:11\"",
            "activity": "主要作為",
            "end": "結局,若沒有答案，請回答未記錄"
         }"""
        },
        {"input":"請列出以色列人離開埃及直到進入嘉南美地主要事件，發生地和大約時間，", 
        "output_jsonblob": """```json
          {"event": "事件",
            "place": "發生地",
            "time": "相對於出埃及的時間",
            "book": "聖經書卷的名字",
            "verse": "章節",
            "scripture": "聖經章節",
            "activity": "主要事件"
         }"""
        }
      ]
    self.examples_template=PromptTemplate(
      input_variables=["input", "output_jsonblob"],
      template="User: {input}\nsuggested Json blob:\n{output_jsonblob}\n"
    )
    #self.examples_template = examples_template
    self.question = ""
    #self.qeustion_template = PromptTemplate(template="User: {self.question}\nSuggested JSON Blob:\n")

    self.few_shot_prompt = FewShotPromptTemplate(
        examples=self.examples,
        example_prompt=self.examples_template,
        prefix="You are an AI assistant. Given a user question, suggest the best JSON structure for the response.\n",
        suffix="User Question: {question}\nSuggested JSON Output:",
        input_variables=["question"],
        example_separator="\n"
    )

  def getAssistant(self, question=None):
    print("getting assistant ...")
    if question is not None:
      self.question = question
      chat = super().getchat()
    if chat is not None:
      formatted_prompt = self.few_shot_prompt.format(question=question)
      #customerMessage = f"\nUser: {question}\nSuggested JSON Blob:\n"
      #message = f"\nSystem: {self.role}\n" + self.examples + customerMessage
      print("prompt:", formatted_prompt)
      response = chat.invoke(formatted_prompt)

      if response is not None:
        return response.content
      else:
        super().setErr("no answer found!")
        return None
    else:
      print(super().err())
      return None
