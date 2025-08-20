from openai_client import agents, ask_gpt
from furhat_remote_api import FurhatRemoteAPI

def main():
    furhat = FurhatRemoteAPI("localhost")

    voices = furhat.get_voices()
    furhat.set_voice(name="Matthew")

    furhat.say(text="Hello!")
    furhat.gesture(name="BrowRaise")

    #agent_manager = agents()

    while True:
        result = furhat.listen()
        user_text = result.message
        if (user_text == "" ):
            continue
        print(f"User said: {user_text}")

        gpt_response = ask_gpt(str(user_text))
        print(f'Responces: {gpt_response}')
        furhat.say(text=gpt_response)



if __name__ == "__main__":
    main()
