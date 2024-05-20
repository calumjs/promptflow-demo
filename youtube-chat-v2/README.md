# Youtube Chat Flow v2
Built on top of the template Chat Flow, Youtube Chat Flow is designed to allow people to ask queries and get them answered by Youtube videos.

Here's how it works:
- **ChatGPT**: Converts the user's chat history into a search query.
- **Python**: Executes a search on YouTube to find relevant videos.
- **Python**: Downloads the transcripts of all the relevant videos found in the search results.
- **Python**: Stores the embeddings of the video transcripts in a local vector database, utilizing caching to prevent re-embedding and improve efficiency.
- **Python**: Performs a similarity search on the local vector database to find the most relevant content related to the user's query.
- **ChatGPT**: Analyzes the retrieved content from multiple sources and generates a comprehensive response, tying together insights extracted from the relevant video transcripts to provide a context-aware answer to the user's question.


## Install Prompt Flow Extension

Before you begin, install the Prompt Flow extension from the Visual Studio Marketplace to integrate directly into your development environment.

Visit: [Prompt Flow Extension](https://marketplace.visualstudio.com/items?itemName=prompt-flow.prompt-flow)

After installation, go to **Quick Access | Install Dependencies** in your IDE to get Python and the necessary Promptflow packages ready.

## Install Prompt Flow Extension

Before you begin, install the Prompt Flow extension from the Visual Studio Marketplace to integrate directly into your development environment.

Visit: [Prompt Flow Extension](https://marketplace.visualstudio.com/items?itemName=prompt-flow.prompt-flow)

After installation, go to **Quick Access | Install Dependencies** in your IDE to get Python and the necessary Promptflow packages ready.

## Create Connection for LLM Tool to Use
You can follow these steps to create a connection required by the LLM tool.

Currently, there are two connection types supported by the LLM tool: "AzureOpenAI" and "OpenAI". If you want to use "AzureOpenAI" connection type, you need to create an Azure OpenAI service first. Please refer to [Azure Open AI Service](https://azure.microsoft.com/en-us/products/cognitive-services/openai-service/) for more details. If you want to use "OpenAI" connection type, you need to create an OpenAI account first. Please refer to [OpenAI](https://platform.openai.com/) for more details.

```bash
# Override keys with --set to avoid yaml file changes
# Create open ai connection
pf connection create --file openai.yaml --set api_key=<your_api_key> --name open_ai_connection

# Create azure open ai connection
# pf connection create --file azure_openai.yaml --set api_key=<your_api_key> api_base=<your_api_base> --name open_ai_connection
```

Note in [flow.dag.yaml](flow.dag.yaml) we are using a connection named `open_ai_connection`.
```bash
# show registered connection
pf connection show --name open_ai_connection
```
Please refer to connections [document](https://promptflow.azurewebsites.net/community/local/manage-connections.html) and [example](https://github.com/microsoft/promptflow/tree/main/examples/connections) for more details.

## Develop a Chat Flow

The most important elements that differentiate a chat flow from a standard flow are **Chat Input**, **Chat History**, and **Chat Output**.

- **Chat Input**: Refers to the messages or queries submitted by users to the chatbot. This is crucial for a successful conversation as it involves understanding user intentions, extracting relevant information, and triggering appropriate responses.

- **Chat History**: Records all interactions between the user and the chatbot, including both user inputs and AI-generated outputs. Maintaining chat history is essential for keeping track of the conversation context and ensuring the AI can generate contextually relevant responses. It is a special type of chat flow input that stores chat messages in a structured format.

- **Chat Output**: Refers to the AI-generated messages sent to the user in response to their inputs. Generating contextually appropriate and engaging chat outputs is vital for a positive user experience.

A chat flow can have multiple inputs, but Chat History and Chat Input are required inputs in a chat flow.

### Example: YouTube Video Query Chat Flow

This flow enables the chatbot to handle queries about YouTube videos effectively. It processes the user's question about a specific video, searches for relevant YouTube content, selects the best video based on the query, retrieves and presents the video transcript, and delivers a detailed response to the user, all integrated into a seamless chat interface.

## Interact with Chat Flow

Promptflow CLI provides a way to start an interactive chat session for chat flow. Customers can use the below command to start an interactive chat session:

```
pf flow test --flow <flow_folder> --interactive
```

After executing this command, customers can interact with the chat flow in the terminal. They can press **Enter** to send the message to the chat flow. Customers can quit with **ctrl+C**.
Promptflow CLI will distinguish the output of different roles by color: <span style="color:Green">User input</span>, <span style="color:Gold">Bot output</span>, <span style="color:Blue">Flow script output</span>, <span style="color:Cyan">Node output</span>.

If the customer adds "--verbose" in the pf command, the output of each step will be displayed.

## Installation
Before using any chat flows, make sure to install all required dependencies:
```
pip install -r requirements.txt
```

This README update provides a clear overview of how to set up, develop, and interact with a chat flow, specifically detailing an example that handles queries related to YouTube videos.
