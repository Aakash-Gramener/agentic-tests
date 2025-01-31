import os
import datetime
from dotenv import load_dotenv
from autogen import ConversableAgent
from autogen import AssistantAgent, UserProxyAgent
from autogen.coding import LocalCommandLineCodeExecutor
from autogen.code_utils import create_virtual_env

# Load environment variables
load_dotenv()

# Get API key from environment variable
LLM_FOUNDRY_API_KEY = os.getenv('LLM_FOUNDRY_API_KEY')
if not LLM_FOUNDRY_API_KEY:
    raise ValueError("LLM_FOUNDRY_API_KEY not found in environment variables")

llm_config = {
    "config_list": [{
        "model": "gpt-4o-mini",
        "api_key": LLM_FOUNDRY_API_KEY,
        "base_url": "https://llmfoundry.straive.com/openai/v1"
    }]
}

venv_dir = ".venv"
venv_context = create_virtual_env(venv_dir)
# Create a temporary directory to store the code files.
# temp_dir = tempfile.TemporaryDirectory()
today = datetime.datetime.now().strftime("%Y-%m-%d")
assistant = AssistantAgent("assistant", llm_config=llm_config)

# Create a local command line code executor.
executor = LocalCommandLineCodeExecutor(
    timeout=10,  # Timeout for each code execution in seconds.
    work_dir="coding",  # Use the temporary directory to store the code files.
    virtual_env_context=venv_context,
)
# Create an agent with code executor configuration.
user_proxy = UserProxyAgent(
    "user_proxy",
    llm_config=False,  # Turn off LLM for this agent.
    code_execution_config={"executor": executor},  # Use the local command line code executor.
    human_input_mode="ALWAYS",  # Always take human input for this agent for safety.
)

user_proxy.initiate_chat(
    assistant,
    message=f"Today is {today}. Write Python code to plot TSLA's and META's "
    "stock price gains YTD, and save the plot to a file named 'stock_gains.png'.",
    # message="How many Wednesdays are there in the date range 1986-11-08 to 2009-07-04?"
)

import shutil
if os.path.exists(venv_dir):
    shutil.rmtree(venv_dir)