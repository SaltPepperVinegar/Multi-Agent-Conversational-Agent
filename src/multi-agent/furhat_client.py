from furhat_remote_api import FurhatRemoteAPI


class Client:
    
    def __init__(self):
        self.furhat = FurhatRemoteAPI("localhost")
        self.furhat.set_voice(name="Matthew")
        pass
    def start(self):
        self.furhat.say(text="Hello from the Virtual Lab!")
        self.furhat.gesture(name="BrowRaise")

    


