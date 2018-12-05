import subprocess
import pigpio
from klick import klick
from loop import Loop

class SooperLooper:

    syncTyp = 1 # 1 = sync to loop 1
    loops = [None] * 3

    def __init__(self):
        self.pauseAllPin = 20

    def start(self):
        self.klick = klick()

    def creatLoops(self, strip, client, piGpio):
        self.loops[0] = Loop(strip, 0, client, self)
        self.loops[0].recordPin = 26
        self.loops[0].pauseStartPin = 19
        self.loops[0].registerInterrupts(piGpio)

        self.loops[1] = Loop(strip, 1, client, self)
        self.loops[1].recordPin = 13
        self.loops[1].pauseStartPin = 6
        self.loops[1].registerInterrupts(piGpio)

        self.loops[2] = Loop(strip, 2, client, self)
        self.loops[2].recordPin = 5
        self.loops[2].pauseStartPin = 21
        self.loops[2].registerInterrupts(piGpio)

        self.registerInterrupts(piGpio)

    def setDefaultValues(self, client):
        self.setSyncTyp(client, 1)

    def setSyncTyp(self, client, typ):
        self.syncTyp = typ
        if self.syncTyp == 1:
            self.klick.stop()
            print("Setting sync typ to 'sync to loop 1'")
            client.send_message("/set", ["sync_source", 1])
            for i,loop in enumerate(self.loops):
                client.send_message("/sl/" + str(i) + "/set", ["quantize", 3])
                client.send_message("/sl/" + str(i) + "/set", ["sync", 1])
                client.send_message("/sl/" + str(i) + "/set", ["playback_sync", 1])
        elif typ == 2:
            print("Setting sync typ to 'klick'")
            self.klick.start()
            client.send_message("/set", ["sync_source", -1])
            for i,loop in enumerate(self.loops):
                client.send_message("/sl/" + str(i) + "/set", ["quantize", 2])
                client.send_message("/sl/" + str(i) + "/set", ["sync", 1])
                client.send_message("/sl/" + str(i) + "/set", ["playback_sync", 1])
        else:
            print("Wrong sync typ")

    def resetLoops(self):
        for loop in self.loops:
            loop.reset()

    def registerInterrupts(self, piGpio):
        piGpio.set_pull_up_down(self.pauseAllPin, pigpio.PUD_UP)
        piGpio.set_glitch_filter(self.pauseAllPin, 500)
        piGpio.callback(self.pauseAllPin, 2, self.pauseAllInterrupt)

    def pauseAllInterrupt(self, gpio, level, tick):
        if level == 0:
            onePlaying = False
            for loop in self.loops:
                if loop.status == 4:
                    onePlaying = True
            if onePlaying:
                for loop in self.loops:
                    loop.mute()
            else:
                print("Else")
                for loop in self.loops:
                    loop.triggerStart()