import os
from dotenv import load_dotenv
from autogen import AssistantAgent, UserProxyAgent

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

assistant = AssistantAgent("assistant", llm_config=llm_config)
user_proxy = UserProxyAgent("user_proxy", llm_config=llm_config, code_execution_config=False)

# Start the chat
user_proxy.initiate_chat(
    assistant,
    message="Tell me a joke about NVDA and TESLA stock prices.",
)
