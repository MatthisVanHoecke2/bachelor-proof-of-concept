from typing import Optional
from fastapi import FastAPI
from llm.model import Model
from pydantic import BaseModel
from llm.modelService import ModelService
import os

app = FastAPI()
model_service = ModelService()

class Prompt(BaseModel):
    value: str

@app.get("/llm/start")
def start_chat():
    return model_service.start_chat()

@app.get("/llm/stop/{uuid}")
def stop_chat(uuid: str):
    return model_service.stop_chat(uuid)

@app.get("/llm/response/{uuid}")
def read_request(uuid: str, prompt: Prompt):
    return model_service.get_response(uuid, prompt)