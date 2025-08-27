from openai import OpenAI
from pydantic import BaseModel
from typing import Optional
import json
import os 
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Agent(BaseModel):
    name: str = "Agent"
    model: str = "gpt-5-nano"
    instructions: str = "You are a helpful Agent"
    tools: list = []

agent_0 = Agent(
    name="Logical Assistant",
    instructions=        
    "You are a logical, the Analytical personality. " 
    "Provide client logical analyse for the topic"
    "Keep answers short and clear: MAX 50 words. ",
    tools=[],
)
agent_1 = Agent(
    name="Emotional  Assistant",
    instructions=    
    "You are an expressive empathetic emotional personality. " 
    "You should provide client some emotional support  "
    "Keep answers short and clear: MAX 50 words. ",
    tools=[],
)

agent_2 = Agent(
    name="Emotional  Assistant",
    instructions=    
    "You are an An outgoing imaginative creative personality."
    "You should provide client some creative ideas"
    "Keep answers short and clear: MAX 50 words. ",
    tools=[],
)

agent_3 = Agent(
    name="Emotional  Assistant",
    instructions=    
    "You are an orchestration agent to select the best responces  "
    "Keep answers short and clear: MAX 50 words. "
    "If more explanation is needed, ask the user before continuing.",
    tools=[],
)




class Response(BaseModel):
    agent: Optional[Agent]
    messages: list


def run_full_turn(agent : Agent, messages):

    current_agent = agent
    num_init_messages = len(messages)
    messages = messages.copy()

    while True:

        # turn python functions into tools and save a reverse map
        tool_schemas = [function_to_schema(tool) for tool in current_agent.tools]
        tools = {tool.__name__: tool for tool in current_agent.tools}

        # === 1. get openai completion ===
        response = client.chat.completions.create(
            model=agent.model,
            messages=[{"role": "system", "content": current_agent.instructions}]
            + messages,
            tools=tool_schemas or None,
        )
        message = response.choices[0].message
        messages.append(message)

        if message.content:  # print agent response
            print(f"{current_agent.name}:", message.content)

        if not message.tool_calls:  # if finished handling tool calls, break
            break

        # === 2. handle tool calls ===

        for tool_call in message.tool_calls:
            result = execute_tool_call(tool_call, tools, current_agent.name)

            if type(result) is Agent:  # if agent transfer, update current agent
                current_agent = result
                result = (
                    f"Transfered to {current_agent.name}. Adopt persona immediately."
                )

            result_message = {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            }
            messages.append(result_message)

    # ==== 3. return last agent used and new messages =====
    return Response(agent=current_agent, messages=messages[num_init_messages:])


import inspect

def function_to_schema(func) -> dict:
    type_map = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",
        dict: "object",
        type(None): "null",
    }

    try:
        signature = inspect.signature(func)
    except ValueError as e:
        raise ValueError(
            f"Failed to get signature for function {func.__name__}: {str(e)}"
        )

    parameters = {}
    for param in signature.parameters.values():
        try:
            param_type = type_map.get(param.annotation, "string")
        except KeyError as e:
            raise KeyError(
                f"Unknown type annotation {param.annotation} for parameter {param.name}: {str(e)}"
            )
        parameters[param.name] = {"type": param_type}

    required = [
        param.name
        for param in signature.parameters.values()
        if param.default == inspect._empty
    ]

    return {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": (func.__doc__ or "").strip(),
            "parameters": {
                "type": "object",
                "properties": parameters,
                "required": required,
            },
        },
    }


def execute_tool_call(tool_call, tools_map):
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)

    print(f"Assistant: {name}({args})")

    # call corresponding function with provided arguments
    return tools_map[name](**args)



agents = [agent_0,agent_1]
if __name__ == "__main__":
    messages = []
    while True:
        messages = []
        user = int(input("Agent: "))
        message = input("Messages: ")
        messages.append({"role": "user", "content": message})
        new_messages = run_full_turn(agents[user], messages)
        print(new_messages.messages[0].content)
