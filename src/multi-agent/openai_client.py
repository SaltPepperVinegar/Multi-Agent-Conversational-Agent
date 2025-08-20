import os
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class agents:
    def __init__(self):
        self.agents = {
            "chatBot1": {
                "name": "Chatbot",
                "instructions": "You are a chatbot agent, make a friendly conversation.",
                "model": "gpt-5-nano",
            },
        }
        self.sessions = {}
        for key, a in self.agents.items():
            sess = client.responses.sessions.create(metadata={"agent": a["name"]})
            self.sessions[key] = sess.id

    def ask_agent(self,user_text, agent_key = "chatBot1"):
        a = self.agents[agent_key]
        session_id = self.sessions[agent_key]
        result = client.responses.create(
            model=a["model"],
            agent={"name": a["name"], "instructions": a["instructions"]},
            session_id=session_id,
            input=user_text
        )
        return result.output_text




def ask_gpt(user_input: str) -> str:

    response = client.responses.create(
        model="gpt-5-nano",
        reasoning={"effort": "low"},
        instructions="Have a friendly Conversation.",
        input=user_input,
    )

    return response.output_text
