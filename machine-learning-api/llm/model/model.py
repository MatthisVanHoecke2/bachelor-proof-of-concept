from langchain.chat_models.ollama import ChatOllama
from llama_index.core.llms.callbacks import llm_completion_callback
import uuid
from rag.pipeline import build_rag_pipeline

# Wrapper class for LLMs
class Model():
  def __init__(self):
    self.messages = [] # List of previous messages
    self.uuid = uuid.uuid4() # Generate unique identifier
    llm = ChatOllama(model="llama2", top_k=10, top_p=0.5) # Create Ollama LLM instance
    self.chat_engine=build_rag_pipeline(llm) # Build pipeline for adding custom data

  def getUUID(self):
    return self.uuid

  def getResponse(self, request):
    # Generate response based on input and chat history
    response = self.chat_engine.invoke({"input": request, "chat_history": self.messages.copy()})

    # Add request and response to message history
    self.messages.append({
      "Human": request,
      "Assistant": response["output"]
    })
    return response