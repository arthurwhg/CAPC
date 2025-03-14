from base import OpenAIChatAgent
import json
from pprint import pprint
import re


class Pastor(OpenAIChatAgent) :

  def __init__(self, apiKey='', model=''):
    sys_prompt = """
    You are a christan pastor. You are asked questions on bible or prayers. 
    Please answer customer questions and using scriptures from the bible as much as possible. 
    if you were not sure about the answer, please answer I do not know
    """
    super().__init__(apiKey, model)
    super().setRole(sys_prompt)
    self.output_json_structure = None
    self.language = None
    super().setLanguage(self.language)

  def setOutputJsonStructure(self, structure=None):
    self.output_json_structure = structure
    return self
  
  def setLanguage(self, language=None):
    self.language = language
    super().setLanguage(language)
    return self

  def getAnswer(self,question=None, jsonblob=None, language=""):
    content = super().ask(question=question, jsonblob=jsonblob, language=language)
    if content is not None:
      if super().getJsonFormat() is not None:
          obj = re.search(r'```json(.*?)```', content, re.DOTALL)
          #answers.append(obj.group(1))
          return json.loads(obj.group(1))
      else:
          return content
    else:
      return None

