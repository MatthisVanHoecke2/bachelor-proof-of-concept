from typing import Union
from fastapi import FastAPI
from model import Model
from pydantic import BaseModel
import os

app = FastAPI()
models = set()
os.environ["OPENAI_API_KEY"] = "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"

class Prompt(BaseModel):
    value: str

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

@app.get("/test")
def test_data(prompt: Prompt):
    selected = Model()
    return selected.get_custom_data(prompt.value)


def find_model(uuid):
    for model in models:
        if(str(model.getUUID()) == uuid):
            return model
    return None