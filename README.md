# Prompt Flow Demo

## Pre-requisites

First, check if Python is already installed on your system. Open your terminal and try running the following commands:

```bash
python --version
```

or

```bash
conda info
```

If these commands do not work, follow the steps below to install Python. You'll need Python 3.9 or later. We recommend using a virtual environment to manage dependencies, such as [Anaconda](https://www.anaconda.com/products/distribution). However, installing Python directly is also acceptable.

Using virtual environments allows you to create isolated environments for different projects, preventing conflicts between dependencies. You can use Anaconda or Python's built-in `venv` module to create virtual environments.

### Option 1: Installing Anaconda with Python

1. **Download and Install Anaconda:**
   - Visit the [Anaconda Distribution page](https://www.anaconda.com/products/distribution).
   - Download the installer for your operating system.
   - Follow the installation instructions on the Anaconda website. (Make sure to check the box that adds Anaconda to your system's PATH during installation)

2. **Verify the Installation:**
   - Open your terminal and run:
     ```bash
     conda --version
     ```
   - This should display the version of Conda installed, confirming that Anaconda is correctly set up.

3. **Setting Up a Virtual Environment (Optional but Recommended):**
   - Create a new virtual environment with Python 3.9 or later:
     ```bash
     conda create --name myenv python=3.9
     conda init
     ```

   - Restart VS Code or the terminal to activate the virtual environment.
   
   - Activate the virtual environment:
     ```bash
     conda activate myenv
     ```

### Option 2: Installing Python Directly

1. **Download Python:**
   - Visit the [Python Downloads page](https://www.python.org/downloads/).
   - Download the installer for Python 3.9 or later for your operating system.
   - Follow the installation instructions on the Python website.

2. **Verify the Installation:**
   - Open your terminal and run:
     ```bash
     python --version
     ```
   - This should display the version of Python installed, confirming that Python is correctly set up.

**Important Note:**

Regardless of how you install Python (via Anaconda or directly), ensure that the Python executable is included in your system's PATH. This allows you to run Python commands from any terminal window.


## Install Prompt Flow Extension

Before beginning any development, install the Prompt Flow extension from the Visual Studio Marketplace to seamlessly integrate it into your development environment. This extension facilitates the creation and management of chat flows directly within your IDE.

Visit: [Prompt Flow Extension](https://marketplace.visualstudio.com/items?itemName=prompt-flow.prompt-flow)

After installation, navigate to **Quick Access | Install Dependencies** in your IDE to prepare Python and the necessary Promptflow packages.

## Create Connection for LLM Tool to Use

To interact with the LLM tool, you must establish a connection. There are two main types of connections:

- **OpenAI**: If you opt for the OpenAI connection type, you will need to create an OpenAI account. Visit [OpenAI](https://platform.openai.com/) for more information.
- **Azure OpenAI**: Alternatively, if you choose this connection type, create an Azure OpenAI service first. For more details, please visit [Azure OpenAI Service](https://azure.microsoft.com/en-us/products/cognitive-services/openai-service/).

Here are the commands to set up these connections:

```bash
# Override keys with --set to avoid yaml file changes
# Create OpenAI connection
pf connection create --file openai.yaml --set api_key=<your_api_key> --name open_ai_connection

# Create Azure OpenAI connection
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

Ask it a question for it to answer by looking up a YouTube video, e.g., "What is Calum's latest video on SSW TV about?"
