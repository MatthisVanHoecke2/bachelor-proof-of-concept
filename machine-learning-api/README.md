# bachelor-proof-of-concept API

This is the back-end of the project, where we run and communicate with the models.

## Table Of Contents
1. [Setup](#Setup)
2. [Running](#Running)
3. [Usage](#Usage)
4. [Technologies](#Technologies)

## Setup
Before starting the API, we need to install all the required packages. To do this, navigate to the folder of this document and run the following command:

    pip install -r requirements.txt

While that is running, we can install the **Ollama** server to communicate with a Large Language Model. Navigate to [Ollama](https://ollama.com/) and click download, then run the installer and wait for the installation to finish. 

## Running
Before we can run our application, we first need to start ollama, if it has not started automatically.

To run Ollama, you have two options:
- Run with the .exe file
- Run from command line

To run it using the .exe file you can do the following:<br>
Search for the Ollama app on your PC, and run it. Nothing will open when running Ollama, this is expected. Ollama will always run in the background on startup.

To run it from command line, open a terminal and run the following command:

    ollama run llama2

After running Ollama, you should be able to start the API using the following command:

    uvicorn main:app --reload

Make sure you run the command from this directory.

## Usage
The following routes are available to communicate with the API:
#### Request
`GET /llm/start` - Starts a new session with a language model

#### Response

    HTTP/1.1 200 OK
    Date: Thu, 24 Feb 2011 12:36:30 GMT
    Status: 200 OK
    Connection: close
    Content-Type: text/plain
    Content-Length: 36
    
    "1e2b49d6-f33c-41f6-b461-1ad2fe7f9574"

#### Request
`GET /llm/stop/{uuid}` - Stops a specific session with a language model

#### Response
    HTTP/1.1 200 OK
    Date: Thu, 24 Feb 2011 12:36:30 GMT
    Status: 200 OK
    Connection: close
    Content-Type: text/plain
    Content-Length: 36

    "Closed chat"

#### Request
`POST /llm/response/{uuid}` - Get a response from a language model

#### Response
    HTTP/1.1 200 OK
    Date: Thu, 24 Feb 2011 12:36:30 GMT
    Status: 200 OK
    Connection: close
    Content-Type: application/json
    Content-Length: 173

    {
      "input":"Who is the author?", 
      "chat_history":[
          {
            "Human":"Hello.",
            "Assistant":"Hello! How can I help you today?"
          }
      ],
      "output":"The author of this project is Matthis Van Hoecke"
    }

## Technologies
[Ollama](https://ollama.com/) - For communicating with a language model<br>
[LlamaIndex](https://docs.llamaindex.ai/en/stable/) - For adding custom data to the language model<br>
[LangChain](https://python.langchain.com/docs/get_started/introduction/) - For getting a more natural response from the language model<br>
[ChromaDB](https://docs.trychroma.com/getting-started) - For creating a vector database from our custom data<br>
[FastAPI](https://fastapi.tiangolo.com/) - For serving the model<br>
[Keras](https://keras.io/api/) - For handling image classification<br>
