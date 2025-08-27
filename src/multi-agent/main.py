from openai_client import *
from furhat_client import *

def main():
    furhat = getFurhat()
    voices = furhat.get_voices()
    furhat.set_voice(name="Matthew")

    furhat.say(text="Hello!")
    furhat.gesture(name="BrowRaise")
    print(furhat.get_gestures)
    #agent_manager = agents()

    while True:
        print("Connected, start listening")
        result = furhat.listen()
        if (result.message == "" or result.success == False):
            continue
        user_text = result.message
        print(result)

        messages = []
        messages.append({"role": "user", "content": user_text})
        new_messages = run_full_turn(agents[0], messages)
        print(f'Responces: {new_messages}')
        furhat.say(text=new_messages.messages[0].content)

if __name__ == "__main__":
    main()
