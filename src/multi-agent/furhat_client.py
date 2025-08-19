from furhat_remote_api import FurhatRemoteAPI


def main():
    # If your SDK + virtual robot run locally:
    furhat = FurhatRemoteAPI("localhost")  # defaults to port 54321

    # Try some calls:
    print(furhat.get_voices())             # list voices
    furhat.set_voice(name="Matthew")       # pick a voice (e.g., Polly voice)
    furhat.say(text="Hello from the Virtual Lab!")
    furhat.gesture(name="BrowRaise")
    result = furhat.listen()               # blocks; returns ASR result
    while True:
        print("Listening...")
        result = furhat.listen()  # blocks until speech is recognized
        print(result)
        
if __name__  == '__main__':
    main()
    



