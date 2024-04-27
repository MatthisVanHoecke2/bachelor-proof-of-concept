# bachelor-proof-of-concept client
This is the front-end of the project, otherwise known as the client.

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
- Chatbot with a Large Language Model (LLM)
- Image Recognition with a Convolutional Neural Network (CNN)

### Large Language model
The author implemented the Large Language Model LLaMa2 from Meta in this application to be used as an AI assistant.<br>
The AI was given a tool so it can access the author's custom data using a text document.

To communicate with the AI, please navigate to the [model's page](https://localhost:7133/llm).<br>

<img src="https://github.com/MatthisVanHoecke2/bachelor-proof-of-concept/assets/101056688/5bccee39-b4ef-474b-8cda-f1b141897417" width="80%"/><br>

Once the model has started, you can send messages through the message box at the bottom of the page. Please wait a while for the AI to respond.<br>

<img src="https://github.com/MatthisVanHoecke2/bachelor-proof-of-concept/assets/101056688/2e9a3c22-103a-41f2-8862-50f271433303" width="80%"/><br>

### Image Recognition
This feature creates or loads a CNN model on startup which is trained on images of flowers to recognize certain characteristics so that it can classify them under one of the following categories: [daisy, dandelion, roses, sunflowers, tulips]<br>

To use this feature, please navigate to the [model's page](https://localhost:7133/cnn).<br>

<img src="https://github.com/MatthisVanHoecke2/bachelor-proof-of-concept/assets/101056688/4c3ca998-441a-49b1-ac3f-992145cd958b" width="80%"/><br>

You can now click the upload button to upload an image to the client. Please make sure it is in png, jpeg or jpg format.<br>

<img src="https://github.com/MatthisVanHoecke2/bachelor-proof-of-concept/assets/101056688/267e0ff7-267a-40b2-97c7-206033f4192d" width="80%"/><br>

After the image has been uploaded, you can send it to the API to be classified by the CNN model by clicking the submit button.<br>

<img src="https://github.com/MatthisVanHoecke2/bachelor-proof-of-concept/assets/101056688/df99ac47-30c8-47f4-86b0-74a12bd0694b" width="80%"/><br>

## Technologies
[.NET](https://dotnet.microsoft.com/en-us/learn/dotnet/what-is-dotnet) - Application platform supported by microsoft<br>
[MudBlazor](https://mudblazor.com/) - Framework for adding premade components
