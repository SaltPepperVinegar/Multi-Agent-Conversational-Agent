import asyncio
from openai import OpenAI
import os 
from agents import Agent, ModelSettings, RunConfig, Runner, function_tool
from memory import SharedMemory

from furhat_client import getFurhat
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

memory = SharedMemory(max_chars=6000)



@function_tool
async def ask_logical(query: str) -> str:
    """Use this for logic/analysis questions."""
    print("asking logical")

    context = memory.render_context()
    r = await Runner.run(
        agent_logical,
        input=f"{context}\n\nUser: {query}"
    )
    memory.add_agent("Logical Assistant", r.final_output)
    return r.final_output

@function_tool
async def ask_emotional(query: str) -> str:
    """Use this for emotional support and empathy."""
    print("asking emotional")
    context = memory.render_context()
    r = await Runner.run(
        agent_emotional,
        input=f"{context}\n\nUser: {query}"
    )
    memory.add_agent("Logical Assistant", r.final_output)
    return r.final_output

@function_tool
async def ask_creative(query: str) -> str:
    """Use this for brainstorming and creative suggestions."""
    print("asking creative")

    context = memory.render_context()
    r = await Runner.run(
        agent_creative,
        input=f"{context}\n\nUser: {query}"
    )
    memory.add_agent("Logical Assistant", r.final_output)
    return r.final_output



@function_tool
def perform_gesture(gesture: str):
    """
    Perform a built-in Furhat gesture.

    Args:
        gesture (str): The name of the gesture to perform. 
            Available gestures include:
            - BigSmile
            - Blink
            - BrowFrown
            - BrowRaise
            - CloseEyes
            - ExpressAnger
            - ExpressDisgust
            - ExpressFear
            - ExpressSad
            - GazeAway
            - Nod
            - Oh
            - OpenEyes
            - Roll
            - Shake
            - Smile
            - Surprise
            - Thoughtful
            - Wink
    """
    getFurhat().gesture(name = gesture)
    print("perform gesture f'{gesture} \n")
    return ""

agent_logical = Agent(
    name="Logical Assistant",
    instructions=        
    "You are a logical, the Analytical personality. " 
    "Provide client logical analyse for the topic"
    "Keep answers short and clear: MAX 50 words. "
    "keep the answer verbal",
    tools =[perform_gesture],
)
agent_emotional = Agent(
    name="Emotional  Assistant",
    instructions=    
    "You are an expressive empathetic emotional personality. " 
    "You should provide client some emotional support  "
    "Keep answers short and clear: MAX 50 words. "
    "keep the answer verbal",
    tools =[perform_gesture],
)

agent_creative = Agent(
    name="Creative  Assistant",
    instructions=    
    "You are an An outgoing imaginative creative personality."
    "You should provide client some creative ideas"
    "Keep answers short and clear: MAX 50 words. "
    "keep the answer verbal",
    tools =[perform_gesture],
)

agent_speaker = Agent(
    name="Speaker",
    instructions=(
        "You are a router. You MUST call EXACTLY ONE tool and you MUST NOT answer directly. "
        "Pass the user's full text to the single best tool and return its result verbatim."
    ),
    tools=[ask_logical, ask_emotional, ask_creative],
)

async def main():
    while True:
        question = await asyncio.to_thread(input, "\nAsk me something: ")

        memory.add_user(question)
        response = await query(question)    
        print(response.final_output)


async def query(user_text):
    memory.add_user(user_text)
    result = await Runner.run(
        agent_speaker,
        input=f"{memory.render_context()}\n\nUser: {user_text}",
        run_config=RunConfig(
            model_settings=ModelSettings(
                tool_choice="required",   # <- key bit
                temperature=0.0           # reduce chatter
            )
        ),
    )
    return result

if __name__ == "__main__":
    asyncio.run(main())



