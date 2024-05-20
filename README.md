# Prompt Flow Demo

## Install Prompt Flow Extension

Before beginning any chat flow development, install the Prompt Flow extension from the Visual Studio Marketplace to seamlessly integrate it into your development environment. This extension facilitates the creation and management of chat flows directly within your IDE.

Visit: [Prompt Flow Extension](https://marketplace.visualstudio.com/items?itemName=prompt-flow.prompt-flow)

After installation, navigate to **Quick Access | Install Dependencies** in your IDE to prepare Python and the necessary Promptflow packages.

## Create Connection for LLM Tool to Use

To interact with the LLM tool, you must establish a connection. There are two main types of connections:

- **OpenAI**: if you opt for the OpenAI connection type, you will need to create an OpenAI account. Visit [OpenAI](https://platform.openai.com/) for more information.
- **AzureOpenAI**: - **OpenAI**: Alternatively, if you choose this connection type, create an Azure OpenAI service first. For more details, please visit [Azure Open AI Service](https://azure.microsoft.com/en-us/products/cognitive-services/openai-service/).

Here are the commands to set up these connections:

```bash
# Override keys with --set to avoid yaml file changes
# Create open ai connection
pf connection create --file openai.yaml --set api_key=<your_api_key> --name open_ai_connection

# Create azure open ai connection
pf connection create --file azure_openai.yaml --set api_key=<your_api_key> api_base=<your_api_base> --name open_ai_connection
```

You can verify your connection setup using:
```bash
# Show registered connection
pf connection show --name open_ai_connection
```

Refer to the connections [documentation](https://promptflow.azurewebsites.net/community/local/manage-connections.html) and [examples](https://github.com/microsoft/promptflow/tree/main/examples/connections) for further details.

## Installation Requirements

Before deploying any chat flows, ensure that all required dependencies are installed. This step is crucial for the smooth functioning of your chat flows.

```bash
pip install -r requirements.txt
```

## Running

To run the flow, use the following command:

```bash
pf flow test --flow ./youtube-chat --interactive
```

And ask it a question for it to answer by looking up a YouTube video, e.g. "What is Calum's latest video on SSWTV about?"
