#from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

class OpenAIChatAgent():

  def __init__(self, apiKey = '', llmModel = '', system_prompt = "" ) :
    self.api_key = apiKey
    self.LLM_Model = llmModel
    self.output = 'plainText'
    self.err = None
    self.question = "who are you and what can you do?"
    self.language = "English"
    self.json_output = ""
    self.customer_prompt = ""
    self.sys_prompt = ""
    self.chatTemplate = None

    if apiKey != "" and llmModel :                                                                                                                                                                                                                                                                                                                                                                             
      self.chat = ChatOpenAI(temperature=0.0, model=llmModel, openai_api_key=apiKey)
    else:
      self.chat = None

    if system_prompt:
      self.sys_prompt = system_prompt

  def setRole(self, system_prompt) :
    self.sys_prompt = system_prompt
    return self

  def setLLMModel(self,model) :
     self.llm_Model = model
     self.chat = ChatOpenAI(temperature=0.0, model=self.llm_Model, openai_api_key=api_key)
     return self

  def getchat(self) :
    return self.chat

  def getModel(self):
    return self.llm_Model

  def setPrompt(self, prompt) :
    self.customer = prompt
    return self

  def setLanguage(self, language) :
    self.language = language
    return self

  def raiseAQuestion(self, question) :
    self.question = question
    return self

  def getJsonFormat(self):
    return self.json_output


  def setJson(self, Jsonblb):
    self.json_output = Jsonblb
    return self


  def _preparePrompts(self, question=None, jsonblob=None, language=""):
    self.question = question if question is not None else None
    self.json_output = jsonblob if jsonblob is not None else None
    self.language = language if language else None
    prompt = self.sys_prompt[1] if self.sys_prompt is not None else ""
    self.sys_prompt = prompt + ". Please answer question in {language} "
    self.customer_prompt = self.customer_prompt + ". Please answer the question: {question}"

    if jsonblob:
      self.customer_prompt = self.customer_prompt + ". please provide your answers in a Json Blob with the structure {jsonblob}"
    
    self.chatTemplate = ChatPromptTemplate.from_messages([self.sys_prompt, self.customer_prompt])


  def printPrompts(self, question=None, jsonblob=None, language=""):
    self._preparePrompts(question, jsonblob, language)
    self.sys_prompt = ("system",self.sys_prompt)  
    self.customer_prompt = ("user",question) 
    #print(self.sys_prompt)
    #print(self.customer_prompt)
    #template = ChatPromptTemplate.from_messages([self.sys_prompt, self.customer_prompt])
    print("System prompt:", self.chatTemplate.messages[0].prompt)
    print("Customer prompt:", self.chatTemplate.messages[1].prompt)
    print("All message:", self.chatTemplate.format_messages(question = self.question, language = "Chinese", jsonblob=self.json_output))

  def getTemplate(self):
    return self.chatTemplate


  def getsystemMessage(self):
    return self.chatTemplate.messages[0].prompt


  def getCustomerMessage(self):
    return self.chatTemplate.messages[1].prompt

  def getMessage(self):
    return self.chatTemplate.format_messages(question = self.question, language = self.language, jsonblob=self.json_output)


  ### 
  #  talk with LLM 
  ###
  def getLLMResponse(self, message):
    try:
      if self.chat is not None:
        return self.chat.invoke(message)
      else:
        self.err = "Model has not been set"
        return None
    except Exception as err:
      self.err = str(err)
      return None

### ask a question and get a answer content in string 
  def ask(self,question=None, jsonblob=None, language=""):
    self._preparePrompts(question, jsonblob, language)
    try:
      if self.chat is None:
        self.err = "Model has not been set"
        return None
    
      if self.chatTemplate is not None:
        message_to_ask = self.chatTemplate.format_messages(question = self.question, language = self.language, jsonblob=self.json_output)
        print("Getting answers ...")
        response = self.chat(message_to_ask)
        print("Got it")
        return response.content
      else:
        self.err = "LLM initiation failed!"
        return None
    except Exception as err:
      self.err = str(err)
      return None
  
  def err(self):
    return self.err


  def setErr(self, err):
    self.err = err
    return self
  

