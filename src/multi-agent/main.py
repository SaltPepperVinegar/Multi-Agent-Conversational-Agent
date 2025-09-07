import asyncio
from speaker_model import query
from furhat_client import *



async def main():
    furhat = getFurhat()
    voices = furhat.get_voices()
    furhat.set_voice(name="Matthew")

    furhat.say(text="Hello!")
    furhat.gesture(name="BrowRaise")
    furhat.get_gestures()

    while True:
        print("Connected, start listening")
        result = furhat.listen()
        if (result.message == "" or result.success == False):
            continue
        user_text = result.message
        print(result)

        response = await query(user_text)

        furhat.say(text=response.final_output)
        print(response.final_output)


if __name__ == "__main__":
    asyncio.run(main())
