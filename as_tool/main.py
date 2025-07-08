import os
from dotenv import load_dotenv
from agents import Agent,Runner, OpenAIChatCompletionsModel,AsyncOpenAI,RunResult, set_tracing_disabled
import rich


load_dotenv()
set_tracing_disabled(disabled=True)
GEMINI_API_KEY=os.getenvenv=("GEMINI_API_KEY"),

client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",

)

shoping_agent = Agent(
    name="shoping-agent",
    instructions="you assist user to finding products and making purchase decisions.",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash-lite", openai_client=client),
    handoff_description="a shoping agent to help user in shoping"



)

support_agent = Agent(
    name="shoping-agent",
    instructions="you help user with post-purchase support and return.",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash-lite", openai_client=client),
    handoff_description="a support agent to help user in post-purchase queries",
)



triage_agent= Agent(
    name="triage_agent",
    instructions=("you are a triage agent, you delegate task to approperiate agent or use appropriate given tools"
                  "when user asked for shoping realated query, you always use given tools"
                  "you never reply on our own, always use given tool to reply user"),
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash-lite", openai_client=client),
    tools = [shoping_agent.as_tool(
        tool_name="transfer_to_shoping_agent",
        tool_description="you assist user to finding products and making purchase decisions.",



    ),
    support_agent.as_tool(
        tool_name="transfer_to_support_agent",
        tool_description="a support agent to help user in post-purchase queries",



    )
             ]

)
result: RunResult = Runner.run_sync(starting_agent=triage_agent, input="i want to return my bag")

rich.print(result.final_output)