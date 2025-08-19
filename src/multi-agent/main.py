from openai_client import chat_with_gpt
from furhat_client import furhat_listen, furhat_speak

def main():
    while True:
        user_text = furhat_listen()
        if user_text.lower() in ["quit", "exit"]:
            break

        gpt_response = chat_with_gpt(user_text)
        furhat_speak(gpt_response)

if __name__ == "__main__":
    main()
