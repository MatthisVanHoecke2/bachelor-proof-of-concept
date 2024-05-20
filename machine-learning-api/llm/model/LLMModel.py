from langchain.chat_models.ollama import ChatOllama
import uuid
from ..rag.pipeline import build_rag_pipeline
import time
import threading

# Timeout in seconds, default 5 minutes
TIMEOUT = 300

# Wrapper class for LLMs
class LLMInstance():
  def __init__(self, stop_callback):
    self.stop_callback = stop_callback
    self.paused = False
    self.messages = [] # List of previous messages
    self.uuid = uuid.uuid4() # Generate unique identifier
    llm = ChatOllama(model="llama2", top_k=10, top_p=0.5) # Create Ollama LLM instance
    self.chat_engine=build_rag_pipeline(llm) # Build pipeline for adding custom data
    self.timer = TIMEOUT
    thread = threading.Thread(target=self.start_timer, args=(), kwargs={})
    thread.start()

  # Start timeout timer, closes session when it hits 0
  def start_timer(self):
    while(self.timer > 0 and self.paused == False):
      time.sleep(1)
      self.timer -= 1
      if(self.timer <= 0):
        self.stop_callback(self.uuid)
        print("Session expired")

  # Reset timeout timer
  def reset_timer(self):
    self.timer = TIMEOUT
    self.paused = False
    thread = threading.Thread(target=self.start_timer, args=(), kwargs={})
    thread.start()

  def getUUID(self):
    return self.uuid

  def getResponse(self, request):
    self.paused = True

    # Generate response based on input and chat history
    response = self.chat_engine.invoke({"input": request, "chat_history": self.messages.copy()})

    # Add request and response to message history
    self.messages.append({
      "Human": request,
      "Assistant": response["output"]
    })

    self.reset_timer()
    return response