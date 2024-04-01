from typing import Union
from fastapi import FastAPI
from model import Model
from pydantic import BaseModel

app = FastAPI()
models = set()

class Prompt(BaseModel):
    value: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/start")
def start_chat():
    model = Model()
    models.add(model)
    return model.getUUID()

@app.get("/stop/{uuid}")
def stop_chat(uuid):
    model = find_model(uuid)
    models.remove(model)
    return "Closed chat"

@app.get("/response/{uuid}")
def read_request(uuid, prompt: Prompt):
    selected = find_model(uuid)
    if(selected is None):
      return "Invalid UUID"
    return selected.getResponse(prompt.value)


def find_model(uuid):
    for model in models:
        if(str(model.getUUID()) == uuid):
            return model
    return None