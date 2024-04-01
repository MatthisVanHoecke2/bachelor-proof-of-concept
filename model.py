from llama_index.llms.ollama import Ollama
from llama_index.core.llms import ChatMessage
import uuid

class Model():
  def __init__(self):
    self.messages = []
    self.uuid = uuid.uuid4()

  def getUUID(self):
    return self.uuid

  def getResponse(self, request):
    llm = Ollama(model="llama2", request_timeout=60.0)

    self.messages.append(ChatMessage(role="user", content=request))
    
    response = llm.chat(
      self.messages
    )

    self.messages.append(ChatMessage(role="assistant", content=response.message.content))
    return response