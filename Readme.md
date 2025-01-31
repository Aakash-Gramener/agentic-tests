# Agentic Code Editor

## Option 1: [Swarm(OpenAI)](https://github.com/openai/swarm)
- Still in experimental stage
- No plans for production
- Does not support custom api urls

## Option 2: [SmolAgents(HuggingFace)](https://github.com/huggingface/smolagents)
- Can be used for production
- Documentation states that openai compatible urls are supported but in reality does not work with custom api urls
- Documentation otherwise is extensive
- Features include Tools, Multiple Agent types,etc

## Option 3: [Autogen(Microsoft)](https://microsoft.github.io/autogen/stable/index.html)
- Can be used for production
- Supports custom api urls
- Documentation is extensive
- Support is ongoing
- Tool usage seems to be simpler than other options

## Option 4: Nvidia Agents
- TO BE TESTED
- Relatively newer according to my knowledge, although has been extensively tested in production

## Option 5: [OpenHands(AllHands)](https://github.com/All-Hands-AI/OpenHands/)
- TO BE TESTED
- Has access to 3 variants:
    - GUI
    - CLI
    - Headless
- Seems to allow custom api urls
- Can be run on github actions
- Can connect to local filesystem
## Final Verdict
- For now, I will be using Autogen as it has the most comprehensive documentation and support.
- If Nvidia Agents proves to be better, I will switch to it.

## Documentation
- In order to use Autogen with custom api urls, you need to use the following code:

```python
llm_config = {
    "config_list": [{
        "model": "gpt-4o-mini",
        "api_key": LLM_FOUNDRY_API_KEY,
        "base_url": "https://llmfoundry.straive.com/openai/v1"
    }]
}
```
Pass this to the llm_config parameter in any agent class that requires an llm otherwise pass False.
Eg:
```python
assistant = AssistantAgent("assistant", llm_config=llm_config)
```

## Types of Agents Used:[Docs](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/agents.html)
### AssistantAgent
### UserProxyAgent
### ConversableAgent

## Code Execution
- Autogen uses a LocalCommandLineCodeExecutor by default.
- This is a wrapper around the code execution.
- Generally it is not advised to use this as library conflicts may arise.
- We can either use docker or use a virtual environment.
- For now, I will be using a virtual environment.
- Here is a template for creating a virtual environment:
```python
import os
import shutil
from autogen.code_utils import create_virtual_env
venv_dir = ".venv"
venv_context = create_virtual_env(venv_dir)

# rest of the code

if os.path.exists(venv_dir):
    shutil.rmtree(venv_dir)
```
- This will create a virtual environment in the current directory and remove it after the code execution is complete.
- The reason for removing the virtual environment is to avoid conflicts with the library.
- If you are using a virtual environment, you need to pass the virtual environment context to the code execution config.
- Eg:
```python
executor = LocalCommandLineCodeExecutor(
    virtual_env_context=venv_context, 
    work_dir="coding")
```
A small test script is provided here: 

## Tests
### Chat Test
- [chat_test.py](chat_test.py)
- This is a simple chat between an assistant and a user.
- I simply let the userproxy initiate a chat with the assistant.
    - "Tell me a joke about NVDA and TESLA stock prices."
- We can also prompt further as shown below:
```
user_proxy (to assistant):

Tell me a joke about NVDA and TESLA stock prices.

--------------------------------------------------------------------------------
assistant (to user_proxy):

Why did NVDA break up with Tesla?

Because it couldn't handle all the "volatility" in their relationship! 

But don't worry, it found a "solid" connection elsewhere! 

TERMINATE

--------------------------------------------------------------------------------
Replying as user_proxy. Provide feedback to assistant. Press enter to skip and use auto-reply, or type 'exit' to end the conversation: Tell me ano
ther joke
user_proxy (to assistant):

Tell me another joke

--------------------------------------------------------------------------------
assistant (to user_proxy):

Why don't NVDA and Tesla tell secrets to each other?

Because they can't keep their "prices" from going up and down!

TERMINATE

--------------------------------------------------------------------------------
Replying as user_proxy. Provide feedback to assistant. Press enter to skip and use auto-reply, or type 'exit' to end the conversation: Tell me a j
oke only about tesla
user_proxy (to assistant):

Tell me a joke only about tesla

--------------------------------------------------------------------------------
assistant (to user_proxy):

Why did the Tesla cross the road?

--------------------------------------------------------------------------------
Replying as user_proxy. Provide feedback to assistant. Press enter to skip and use auto-reply, or type 'exit' to end the conversation: Tell me a joke only about tesla
user_proxy (to assistant):

Tell me a joke only about tesla

--------------------------------------------------------------------------------
assistant (to user_proxy):

Why did the Tesla cross the road?
user_proxy (to assistant):

Tell me a joke only about tesla

--------------------------------------------------------------------------------
assistant (to user_proxy):

Why did the Tesla cross the road?
--------------------------------------------------------------------------------
assistant (to user_proxy):

Why did the Tesla cross the road?

Why did the Tesla cross the road?
Why did the Tesla cross the road?


To recharge its battery on the other side!


TERMINATE

--------------------------------------------------------------------------------
Replying as user_proxy. Provide feedback to assistant. Press enter to skip and use auto-reply, or type 'exit' to end the conversation: exit       
PS C:\Gramener\Agents_Comp>
```
### Code execution
- Reference for documentation: [Code Execution](https://microsoft.github.io/autogen/0.2/docs/tutorial/code-executors/)
- [code_execution_test.py](code_execution_test.py)
- This is a simple code execution test.
- I use a virtual environment and a simple prompt to test the code execution.
```python
user_proxy.initiate_chat(
    assistant,
    message=f"Today is {today}. Write Python code to plot TSLA's and META's "
    "stock price gains YTD, and save the plot to a file named 'stock_gains.png'.",
)
```
- After a few iterations a suitable script has been generated.
- The script is saved as [./coding/plot_stock_gains.py](./coding/plot_stock_gains.py)
- The script is then executed and the plot is saved as [./coding/stock_gains.png](./coding/stock_gains.png)
- The virtual environment ensures that there is no conflict with the global library space and the environment is cleaned up after the code execution is complete.
- The code execution is done using the LocalCommandLineCodeExecutor.
- WARNING: Have had problems with libraries not being found in the environment.

### Error Detection
- I have taken a small python script[leaderboard.py](leaderboard.py) from one of my projects and introduced multiple syntax errors in it.
- For now I have used a script manually to convert the code into text and then pass it to the agents.
- The Agents are able to identify the syntax errors and fix them.
- Planning on testing and developing the following features:
    - Logical Errors
    - Runtime Errors
    - Refactoring
    - Tool usage so that the user can tell which files to edit
    - Let the system ask the user for input files for the code to be executed

## Tool Usage
- [Autogen_tool_test.py](Autogen_tool_test.py)
- This is a simple test to see if the tool usage works.
- The tool is registered using the register_for_execution decorator.
- The tool is then used in the chat.
- The example is a simple calculator.
- The assistant determines the parameters for the tool and the userproxy executes the tool.

## Code Critique
- [autogen_code_critic.py](autogen_code_critic.py)
- Here we use 3 agents to critique the code.
- The first agent is the userproxy agent which is the user.
- The second agent is the coder agent which is the assistant that writes the code.
- The third agent is the critic agent which is the assistant that critiques the code.
- The critique is then used to improve the code. Keep in mind that the critique does not provide any code but provides metrics for the code and suggestions for improvement.
- The code is then edited by the coder agent and the process is repeated.
- The process is repeated until the code is satisfactory.
- Prompt:
```python
user_proxy.initiate_chat(
    manager,
    message="download data from https://raw.githubusercontent.com/uwdata/draco/master/data/cars.csv and plot a visualization that tells us about the relationship between weight and horsepower. Save the plot to a file. Print the fields in a dataset before visualizing it.",
)
```
- Output: [weight vs horsepower.png](./groupchat/weight_vs_horsepower.png)

## Auto Edit
- [autogen_auto_edit.py](autogen_auto_edit.py)
- In this example I attempt to let the agent access a file and edit it.
- Multiple agents are used to achieve this.
- The initiator agent is the user.
- The assistant agent is the assistant that accesses the file.
- The coder agent is the assistant that edits the code.
- The critic agent is the assistant that critiques the code.
- The code is then edited by the coder agent and the process is repeated.
- The process is repeated until the code is satisfactory.
- There is a issue with the agent transfer sequence.
- The conversation is abruptly transfered to the assistant agent, even when there is no request for it.
- Changes to the description of the agents may help but haven't been able to find a solution yet.
- There also seems to be an issue where the code is saved as a tmp-<...>.py file. This is turn, doesn't get executed.

