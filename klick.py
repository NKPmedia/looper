from pythonosc import udp_client

class klick:

    def __init__(self):
        self.client = udp_client.SimpleUDPClient("127.0.0.1", 9953)

    def start(self):
        self.client.send_message("/klick/metro/set_type", "simple")
        self.client.send_message("/klick/metro/start",[])
        self.client.send_message("/klick/simple/set_tempo", 120)
        self.client.send_message("/klick/simple/set_meter", [4,4])
    def stop(self):
        self.client.send_message("/klick/metro/stop",[])
    def setTempo(self, tempo):
        self.client.send_message("/klick/simple/set_tempo", tempo)
    def setVolume(self, vol):
        self.client.send_message("/klick/config/set_volume", vol)
