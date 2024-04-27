# bachelor-proof-of-concept client
This is the front-end of the project, otherwise known as the web application.

## Setup - Mac
Before starting the client, we need to install dotnet on our pc. Navigate to [this page](https://dotnet.microsoft.com/en-us/download) and download dotnet.

## Running
The client application does not need additional setup and works out-of-the-box.<br>
Before running the application, please make sure your terminal is located in the current directory.

To start the application, please execute the following command:

    dotnet run --project "src/Client"

The client can now be viewed at https://localhost:7133

## Usage
The author has added two main features for this proof-of-concept project:
- Chatbot with a Large Language Model
- Image Recognition with a Convolutional Neural Network

### Large Language model
The author implemented the Large Language Model LLaMa2 from Meta in this application to be used as an AI assistant.<br>
The AI was given a tool so it can access the author's custom data using a text document.

To communicate with the AI, please navigate to the [model's page](https://localhost:7133/llm).<br>

<img src="https://github.com/MatthisVanHoecke2/bachelor-proof-of-concept/assets/101056688/5bccee39-b4ef-474b-8cda-f1b141897417" width="80%"/><br>

Once the model has started, you can send messages through the message box at the bottom of the page. Please wait a while for the AI to respond.<br>

<img src="https://github.com/MatthisVanHoecke2/bachelor-proof-of-concept/assets/101056688/2e9a3c22-103a-41f2-8862-50f271433303" width="80%"/><br>


## Technologies
[.NET](https://dotnet.microsoft.com/en-us/learn/dotnet/what-is-dotnet) - Application platform supported by microsoft
[MudBlazor](https://mudblazor.com/) - Framework for adding premade components
