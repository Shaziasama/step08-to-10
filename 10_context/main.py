from dotenv import load_dotenv
from agents import Agent , Runner ,OpenAIChatCompletionsModel , AsyncOpenAI , set_tracing_disabled, RunContextWrapper,function_tool

import rich
import os
from pydantic import BaseModel

load_dotenv()
set_tracing_disabled(disabled=True)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class User_info(BaseModel):
    name: str
    age: int
    alive: bool
    roll_no: str

my_info = User_info(name="Zohaib", age=25, alive=True, roll_no="12345")


client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

def dynamic_ins(wrapper: RunContextWrapper[User_info], agent: Agent[User_info]):
    return (
        f"user name is {wrapper.context.name}, "
        f"user age is {wrapper.context.age}, "
        f"user roll no is {wrapper.context.roll_no}, "
        f"user is alive: {wrapper.context.alive}"
    )


@function_tool
async def zohaib_information(wrapper: RunContextWrapper[User_info]): 
    """This function tells about Zohaib's roll number"""
    return f"user roll no is {wrapper.context.roll_no}"





agent = Agent[User_info](
    name="Agent",
    instructions=dynamic_ins,
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    tools=[zohaib_information],


)

result = Runner.run_sync(agent, input="what is name of user and his roll number?", context=my_info)
rich.print(result.final_output)
