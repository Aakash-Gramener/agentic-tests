import os
from autogen import AssistantAgent, UserProxyAgent
from dotenv import load_dotenv

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

# assistant = AssistantAgent("assistant", llm_config=llm_config)
# user_proxy = UserProxyAgent("user_proxy", code_execution_config=False)

# # Start the chat
# user_proxy.initiate_chat(
#     assistant,
#     message="Tell me a joke about NVDA and TESLA stock prices.",
# )


import os
import autogen
from autogen import AssistantAgent, UserProxyAgent
from autogen.code_utils import create_virtual_env

venv_dir = ".venv"
venv_context = create_virtual_env(venv_dir)
# llm_config = {"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}
assistant = AssistantAgent("assistant", llm_config=llm_config)

user_proxy = UserProxyAgent(
    "user_proxy",
    system_message="You are a code editor. There are errors in the code. Fix the errors and return and save the corrected code. If any files are missing, prompt the user for those files and inform them the correct path to the file.",
    code_execution_config={"executor": 
                            autogen.coding.LocalCommandLineCodeExecutor(
                                    virtual_env_context=venv_context, 
                                    work_dir="coding")}
)

def save_file_as_text(input_file, output_file):
    """
    Reads the contents of a file and saves it to another file.

    Args:
        input_file (str): The path to the input file to be read.
        output_file (str): The path to the output file where content will be saved.

    Returns:
        str: A success message if the operation completes successfully.
    """
    try:
        # Open and read the contents of the input file
        with open(input_file, 'r') as file:
            content = file.read()

        # Write the content to the output file
        with open(output_file, 'w') as file:
            file.write(content)

        # return f"Contents of '{input_file}' saved to '{output_file}' successfully."
        return content

    except FileNotFoundError:
        return f"Error: The file '{input_file}' does not exist."
    except Exception as e:
        return f"An error occurred: {e}"
    
code_content = save_file_as_text("leaderboard.py", "leaderboard_output.txt")
print(code_content)
# Start the chat
user_proxy.initiate_chat(
    assistant,
    # message="Plot a chart of NVDA and TESLA stock price change YTD.",
    message=code_content
)

# Clean up the virtual environment
import shutil
if os.path.exists(venv_dir):
    shutil.rmtree(venv_dir)