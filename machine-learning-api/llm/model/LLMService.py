from typing import Optional
from .LLMModel import LLMInstance
from pydantic import BaseModel

# Prompt dto for passing a prompt to the LLM
class Prompt(BaseModel):
    value: str

# Service class for keeping track of multiple models
class LLMService:
  def __init__(self):
    self.models = set()

  # Start chat with a model and return a unique identifier
  def start_chat(self):
    model = LLMInstance(self.stop_chat)
    self.models.add(model)
    print(model.getUUID())
    return model.getUUID()
  
  # Remove a model from the list of active models
  def stop_chat(self, uuid):
    model = self.__find_model(uuid)
    for model in self.models: # For some reason callback won't remove model without this bit of code
       counter = 1
    if(model is not None):
      self.models.remove(model)
    return "Closed chat"

  # Generate a response based on a given prompt
  def get_response(self, uuid: str, prompt: Prompt):
    selected: Optional[LLMInstance] = self.__find_model(uuid)
    if(selected is None):
      return "Invalid UUID"
    return selected.getResponse(prompt.value)

  # Find model in list of active models based on uuid
  def __find_model(self, uuid: str) -> Optional[LLMInstance]:
    for model in self.models:
        if(str(model.getUUID()) == uuid):
            return model
    return None