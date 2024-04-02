from typing import Optional
from llm.model import Model
from pydantic import BaseModel

class Prompt(BaseModel):
    value: str

class ModelService:
  def __init__(self):
    self.models = set()

  def start_chat(self):
    model = Model()
    self.models.add(model)
    return model.getUUID()
  
  def stop_chat(self, uuid):
    model = self.__find_model(uuid)
    self.models.remove(model)
    return "Closed chat"

  def get_response(self, uuid: str, prompt: Prompt):
    selected: Optional[Model] = self.__find_model(uuid)
    if(selected is None):
      return "Invalid UUID"
    return selected.getResponse(prompt.value)

  def __find_model(self, uuid: str) -> Optional[Model]:
    for model in self.models:
        if(str(model.getUUID()) == uuid):
            return model
    return None