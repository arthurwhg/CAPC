from base import OpenAIChatAgent
from langchain.prompts import FewShotPromptTemplate, PromptTemplate
from langchain.schema import AIMessage, HumanMessage, SystemMessage
import json
from pprint import pprint
import re


class FewShotsChatAgent(OpenAIChatAgent) :

  ##
  #
  # examples: multi shots examples
  #    [ {"input":"", "output": ""},
  #      {"input":"", "output": ""},
  #      {"input":"", "output": ""}
  #    ]
  # example_prompt: PromptTemplate
  #    promptTemplate(
  #     input_variables=["input", "output"],
  #     template="User: {input}\nAI: {output}\n"
  # )                                                                                                                                                                                                                                                                                                                                                                                                    
  ##
  def __init__(self, apiKey='', model='', role="", examples=None, examples_prompt=None):
    super().__init__(apiKey, model)
    self.examples = examples
    self.examples_prompt = examples_prompt
    self.role = role
    #super().setRole(role)
    self._createFew_shot_prompt


  def _createFew_shot_prompt(self):
    self.few_shot_prompt = FewShotPromptTemplate(
          examples=self.examples,  # List of examples
          example_prompt=self.examples_prompt,  # Template for formatting examples
          prefix=self.role,
          suffix="User: {question}\nAI:",  # This is where the actual question goes
          input_variables=["question"],  # The final query placeholder
          example_separator="\n"
    )
    return self


  def setExamples(self, examples=None):
    if examples is not None:
      self.examples = examples
      self._createFew_shot_prompt()
    return self


  def _preparePrompts(self, question=None, jsonblob=None, language=""):
    #return super()._preparePrompts(question, jsonblob, language)
    self.question = question if question is not None else None
    super().setJson(jsonblob if jsonblob is not None else None)
    super().setLanguage(language if language else None)
    self._createFew_shot_prompt()


  def ask(self,question=None, jsonblob=None, language=""):
    self._preparePrompts(question, jsonblob, language)

    print("asking assistant agent ... ")
    try:
      # Generate the formatted prompt
      print(" generating prompt ....1")
      final_prompt = self.few_shot_prompt.format(question=question)
      print("📝 Generated Prompt:\n", final_prompt)

      # Initialize an OpenAI model (Replace `your_api_key` with an actual OpenAI API key)
      chat = super().getchat()

      # Get the LLM response
      print("Getting assistant from LLM ...")
      response = chat([HumanMessage(content=final_prompt)])
      print("Got it ....")
      print("💡 LLM Response:\n", response.content)

      return response.content
    
    except Exception as err:
      print("error found xxx", str(err))
      super().setErr(str(err))
      return None
  
  