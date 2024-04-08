from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from llm.model.model import Model
from pydantic import BaseModel
from llm.model.modelService import ModelService, Prompt
import os

# Create a FastAPI instance
app = FastAPI()

# Allow cors cross-origins
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create ModelService instance
model_service = ModelService()

# Create a new llm instance and return a unique identifier
@app.get("/llm/start")
def start_chat():
    return model_service.start_chat()

# Stop an existing chat instance and remove it from the list of active models
@app.get("/llm/stop/{uuid}")
def stop_chat(uuid: str):
    return model_service.stop_chat(uuid)

# Generate a response based on the given prompt
@app.post("/llm/response/{uuid}")
def read_request(uuid: str, prompt: Prompt):
    return model_service.get_response(uuid, prompt)