import os
from autogen import AssistantAgent, UserProxyAgent, ConversableAgent, GroupChat, GroupChatManager
from autogen.coding import LocalCommandLineCodeExecutor
from autogen.code_utils import create_virtual_env
from dotenv import load_dotenv

# Load environment variables from .env file
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
    }],
    # "cache_seed": 42,
}

venv_dir = ".venv"
venv_context = create_virtual_env(venv_dir)


def save_file_as_text(input_file: str, output_file: str) -> str:
        """
        Reads the contents of a file and saves it to another file.

        Args:
            input_file (str): The path to the input file to be read.
            output_file (str): The path to the output file where content will be saved.

        Returns:
            str: The content of the file.
        """
        try:
            # Open and read the contents of the input file
            with open(input_file, 'r') as file:
                content = file.read()

            # Write the content to the output file
            with open(output_file, 'w') as file:
                file.write(content)
            return content
            # return f"Contents of '{input_file}' saved to '{output_file}' successfully."

        except FileNotFoundError:
            return f"Error: The file '{input_file}' does not exist."
        except Exception as e:
            return f"An error occurred: {e}"
        
def return_file_as_text(input_file: str) -> str:
    """
    Reads the contents of a file and returns it as a string with the filename at the beginning.
    """
    with open(input_file, 'r') as file:
        content = file.read()
    return f"File: {input_file}\n\n```{content}```"

def install_libraries(libraries: str) -> str:
    """
    Installs a list of libraries.
    """
    for library in libraries:
        os.system(f"pip install {library}")
    return f"Libraries {libraries} installed successfully."

# if not os.path.exists("file_access"):
#     os.makedirs("file_access")

executor = LocalCommandLineCodeExecutor(
    timeout=30,  # Timeout for each code execution in seconds.
    work_dir="file_access",  # Use the temporary directory to store the code files.
    virtual_env_context=venv_context,
)

initiator = ConversableAgent(
    name="Initiator",
    system_message="You are the initiator. You are responsible for starting the conversation and forging the path for the coder to follow.",
    llm_config=llm_config,
)
user_proxy = UserProxyAgent(
    name="User_proxy",
    system_message="Executor. Executes code written by the coder and if file access is needed, uses the assistant to access files.",

    code_execution_config={
        "last_n_messages": 3,
        "executor": executor,
    },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
    human_input_mode="ALWAYS",
)
coder = AssistantAgent(
    name="Coder",  # the default assistant agent is capable of solving problems with code
    system_message="You are the coder. Given a task, you write python/shell code to solve it.Provide a script to install libraries if needed.",
    llm_config=llm_config,
)
# Let's first define the assistant agent that suggests tool calls.
assistant = ConversableAgent(
    name="Assistant",
    system_message="You help with accessing files. "
    "Return 'TERMINATE' when the task is done.",
    llm_config=llm_config,
)
critic = AssistantAgent(
        name="Critic",
        system_message="""Critic. You are a helpful assistant highly skilled in evaluating the quality of a given visualization code by providing a score from 1 (bad) - 10 (good) while providing clear rationale. YOU MUST CONSIDER VISUALIZATION BEST PRACTICES for each evaluation. Specifically, you can carefully evaluate the code across the following dimensions
    - bugs (bugs):  are there bugs, logic errors, syntax error or typos? Are there any reasons why the code may fail to compile? How should it be fixed? If ANY bug exists, the bug score MUST be less than 5.
    - Data transformation (transformation): Is the data transformed appropriately for the visualization type? E.g., is the dataset appropriated filtered, aggregated, or grouped  if needed? If a date field is used, is the date field first converted to a date object etc?
    - Goal compliance (compliance): how well the code meets the specified visualization goals?
    - Visualization type (type): CONSIDERING BEST PRACTICES, is the visualization type appropriate for the data and intent? Is there a visualization type that would be more effective in conveying insights? If a different visualization type is more appropriate, the score MUST BE LESS THAN 5.
    - Data encoding (encoding): Is the data encoded appropriately for the visualization type?
    - aesthetics (aesthetics): Are the aesthetics of the visualization appropriate for the visualization type and the data?

    YOU MUST PROVIDE A SCORE for each of the above dimensions.
    {bugs: 0, transformation: 0, compliance: 0, type: 0, encoding: 0, aesthetics: 0}
    Do not suggest code.
    Finally, based on the critique above, suggest a concrete list of actions that the coder should take to improve the code.
    """,
        llm_config=llm_config,
    )


# assistant.register_for_llm(name="save_file_as_text", description="Access a file and return the content")(save_file_as_text)
# user_proxy.register_for_execution(name="save_file_as_text")(save_file_as_text)
# assistant.register_for_llm(name="install_libraries", description="Install a list of libraries")(install_libraries)
# user_proxy.register_for_execution(name="install_libraries")(install_libraries)
assistant.register_for_llm(name="return_file_as_text", description="Access a file and return the content")(return_file_as_text)
user_proxy.register_for_execution(name="return_file_as_text")(return_file_as_text)

initiator.description = "Initiator. Starts the conversation.."
user_proxy.description = "Executes code written by the coder. If and only if the user gives a file name, file access is needed, uses the assistant to access files."
coder.description = "Solves problems with code. Provide a script to install libraries if needed."
assistant.description = "Uses tools to access files."
critic.description = "Criticizes the code and provides a score and a list of actions to take. Include any libraries to install."

allowed_transitions = {
    initiator: [assistant],
    user_proxy: [critic],
    assistant: [coder],
    coder: [user_proxy],
    critic: [coder],
}
# def state_transition(last_speaker, groupchat):
#     messages = groupchat.messages

#     if last_speaker is assistant:
#         # init -> retrieve
#         return user_proxy
#     elif last_speaker is coder:
#         # retrieve: action 1 -> action 2
#         return executor
#     elif last_speaker is executor:
#         if messages[-1]["content"] == "exitcode: 1":
#             # retrieve --(execution failed)--> retrieve
#             return coder
#         else:
#             # retrieve --(execution success)--> research
#             return scientist
#     elif last_speaker == "Scientist":
#         # research -> end
#         return None
    
groupchat = GroupChat(
    agents=[initiator, user_proxy, coder, assistant, critic],
    allowed_or_disallowed_speaker_transitions=allowed_transitions,
    speaker_transitions_type="allowed",
    messages=[], 
    max_round=20,
    send_introductions=True,
                    )
manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

initiator.initiate_chat(
    manager,
    message="Take a look at the code plot_stock_error.py and fix the errors. Return and save the corrected code and and save any output.",
)


import shutil
if os.path.exists(venv_dir):
    shutil.rmtree(venv_dir)