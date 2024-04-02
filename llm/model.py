from llama_index.core.llms import ChatMessage
from llama_index.core.indices.struct_store import JSONQueryEngine
from llama_index.core.indices import VectorStoreIndex
from llama_index.core import SimpleDirectoryReader, Settings
from llama_index.core.chat_engine import CondenseQuestionChatEngine
from langchain.chat_models.ollama import ChatOllama
from langchain.chains.conversation.memory import ConversationBufferMemory
from llama_index.core.llms import (
    CustomLLM,
    CompletionResponse,
    CompletionResponseGen,
    LLMMetadata,
)
from llama_index.core.llms.callbacks import llm_completion_callback
import uuid
from rag.pipeline import build_rag_pipeline

class Model():
  def __init__(self):
    self.messages = ConversationBufferMemory()
    self.uuid = uuid.uuid4()
    llm = ChatOllama(model="llama2", top_k=3)
    self.chat_engine=build_rag_pipeline(llm)

  def getUUID(self):
    return self.uuid
  
  def get_custom_data(self, request):
    text = self.chat_engine.invoke({"input": request})
    print(text)
    return text

  def getResponse(self, request):
    response = self.chat_engine.invoke({"input": request, "chat_history": {}})
    return response