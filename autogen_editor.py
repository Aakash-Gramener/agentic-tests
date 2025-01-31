import os
from autogen import AssistantAgent, UserProxyAgent, ConversableAgent
from autogen.code_utils import create_virtual_env
from autogen.coding import LocalCommandLineCodeExecutor
import tempfile
from dotenv import load_dotenv

venv_dir = ".venv"
venv_context = create_virtual_env(venv_dir)
temp_dir = tempfile.TemporaryDirectory()

# Load environment variables
load_dotenv()

# Get API key from environment variable
LLM_FOUNDRY_API_KEY = os.getenv('LLM_FOUNDRY_API_KEY')
if not LLM_FOUNDRY_API_KEY:
    raise ValueError("LLM_FOUNDRY_API_KEY not found in environment variables")

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

        return f"Contents of '{input_file}' saved to '{output_file}' successfully."

    except FileNotFoundError:
        return f"Error: The file '{input_file}' does not exist."
    except Exception as e:
        return f"An error occurred: {e}"
    

llm_config = {
    "config_list": [{
        "model": "gpt-4o-mini",
        "api_key": LLM_FOUNDRY_API_KEY,
        "base_url": "https://llmfoundry.straive.com/openai/v1"
    }]
}

assistant = ConversableAgent(
    name="Assistant",
    system_message="You are a helpful AI assistant. "
    "You can access code files and edit them. "
    "You can also run code files and if there are any errors, fix them and return the corrected code. "
    "Return 'TERMINATE' when the task is done.",
    llm_config= llm_config,
)

user_proxy = ConversableAgent(
    name="User",
    llm_config=False,
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    human_input_mode="NEVER",
)

assistant.register_for_llm(name="code handler", description="Saves the code as text")(save_file_as_text)
user_proxy.register_for_execution(name="code handler")(save_file_as_text)

executor = LocalCommandLineCodeExecutor(
    timeout=10,  # Timeout for each code execution in seconds.
    virtual_env_context=venv_context, 
    work_dir=temp_dir.name,  # Use the temporary directory to store the code files.
)


code_executor_agent = ConversableAgent(
    "code_executor_agent",
    llm_config=False,  # Turn off LLM for this agent.
    code_execution_config={"executor": executor},  # Use the local command line code executor.
    human_input_mode="ALWAYS",  # Always take human input for this agent for safety.
)

chat_result = user_proxy.initiate_chat(assistant, message="Fix the errors in leaderboard.py and return the corrected code.")
print(chat_result)


