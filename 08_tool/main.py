import os
from dotenv import load_dotenv
from agents import Agent, Runner, set_tracing_disabled, OpenAIChatCompletionsModel, AsyncOpenAI, function_tool
import rich

load_dotenv
set_tracing_disabled(disabled=True)
OPENROUTER_API_KEY=os.getenv("OPENROUTER_API_KEY")

@function_tool
def karachi_weather(city: str):
    """
    Get the current weather of karachi.
    """
    return f"the current weather {city} is -0C"




client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

agent = Agent(
    name="my_agent",
    instructions="you are a helpful assistant",
    model=OpenAIChatCompletionsModel(model="mistralai/mistral-small-3.1-24b-instruct:free", openai_client=client),
    
    tools= [karachi_weather]
)

result = Runner.run_sync(agent, "what is the weather of karachi?")
rich.print(result.final_output)
