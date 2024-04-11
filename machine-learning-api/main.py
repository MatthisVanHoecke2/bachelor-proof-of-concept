from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from llm.model.LLMService import LLMService, Prompt
from cnn.model.CNNModel import CNNModel
import io

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

# Create LLMService instance
model_service = LLMService()

# Create CNNModel instance
cnn_model = CNNModel()

@app.post("/cnn/upload")
async def upload(file: UploadFile = File()):
    return cnn_model.predict_data(file)

# Create a new llm instance and return a unique identifier
@app.get("/llm/start")
async def start_chat():
    return model_service.start_chat()

# Stop an existing chat instance and remove it from the list of active models
@app.get("/llm/stop/{uuid}")
async def stop_chat(uuid: str):
    return model_service.stop_chat(uuid)

# Generate a response based on the given prompt
@app.post("/llm/response/{uuid}")
async def read_request(uuid: str, prompt: Prompt):
    return model_service.get_response(uuid, prompt)