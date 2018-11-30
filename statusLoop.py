import threading
import time
from mcp3008 import MCP3008

class StatusLoop(threading.Thread):
    def __init__(self, loops, client):
        threading.Thread.__init__(self)
        self.loops = loops
        self.client = client

    def run(self):
        adc = MCP3008()
        while True:
            for i, loop in enumerate(self.loops):
                loop.getStatus()
            time.sleep(0.08)
            #value = adc.read(channel=4)  # Den auszulesenden Channel kannst du natürlich anpassen
            #print("Anliegende Spannung: %.2f" % (value / 4095.0 * 5))