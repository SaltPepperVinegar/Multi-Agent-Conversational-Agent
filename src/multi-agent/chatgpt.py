import os
from openai import OpenAI


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def ask_chatbot(user_text: str) -> str:
    r = client.responses.create(
        model="gpt-5-nano",
        input=[
            {"role":"system","content":"You are a concise, friendly assistant."},
            {"role":"user","content":user_text},
        ],
    )
    return r.output_text


def main():
    string = input("Say something to the chatbot (Press Enter to exit): ")
    print(ask_chatbot(string))

if __name__  == '__main__':
    print(main())
    

