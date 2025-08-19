import os
from openai import OpenAI


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def chat_gpt(user_input) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # or "gpt-4.1" depending on your needs
        messages=[
            {"role": "system", "content": "You are a helpful conversational agent."},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content

def main():
    string = input("Say something to the chatbot (Press Enter to exit): ")
    print(ask_chatbot(string))

if __name__  == '__main__':
    print(main())
    

