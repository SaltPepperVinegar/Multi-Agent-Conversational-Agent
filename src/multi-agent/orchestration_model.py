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

orchestrator_agent = Agent(
    name="Orchestrator",
    instructions=(
        "You are a summarizer. You will receive the user's query and several "
        "candidate answers from different agents. Your job is to combine their ideas "
        "Less relevant response gets less attention"
        "Keep it verbal"
        "into a single, clear, concise summary that covers the most important points. "
        
    ),
)

agents = [agent_logical, agent_creative, agent_emotional]

async def main():
    while True:
        question = await asyncio.to_thread(input, "\nAsk me something: ")

        memory.add_user(question)
        response = await query(question)    
        print(response.final_output)

async def query(user_text):
    memory.add_user(user_text)

    tasks = [
        Runner.run(
            agent,
            input= f"{memory.render_context()}\n\nUser: {user_text}",
        )
        for agent in agents
    ]

    results = await asyncio.gather(*tasks, return_exceptions=False)

    candidates = []
    for agent, res in zip(agents, results):
        text = (res.final_output or "").strip()
        candidates.append((agent.name, text))

    bundle = "\n\n".join(
        f"[{name}]\n{text}" for name, text in candidates
    )
    print(bundle)
    orchestrator_input = (
        f"{memory.render_context()}\n\n"
        f"User: {user_text}\n\n"
        f"Candidate answers from different agents:\n{bundle}\n\n"
        f"Summarize these into one clear, concise response for the user."
    )

    orchestrator_result = await Runner.run(
        orchestrator_agent,
        input=orchestrator_input
    )
    
    response = orchestrator_result
    
    memory.add_agent("Orchestrator", response.final_output)

    return response

if __name__ == "__main__":
    asyncio.run(main())



