import pigpio
from ring import Ring
from pythonosc import udp_client
import time

class Loop:
    
    number = 0
    recordPin = 0
    pauseStartPin = 0
    loopLen = 1
    status = -1
    pausePressTime = 0

    def __init__(self, strip, number, oscClient:udp_client, sooperlooper):
        self.sooperlooper = sooperlooper
        self.ring = Ring(strip, number)
        self.number = number
        self.oscClient = oscClient
        self.ring.setColor(0, 0, 0)
        self.deleted = 1

    def registerInterrupts(self, piGpio):
        piGpio.set_pull_up_down(self.recordPin, pigpio.PUD_UP)
        piGpio.set_glitch_filter(self.recordPin, 500)
        piGpio.set_pull_up_down(self.pauseStartPin, pigpio.PUD_UP)
        piGpio.set_glitch_filter(self.pauseStartPin, 500)
        piGpio.callback(self.recordPin, 2, self.recordInterrupt)
        piGpio.callback(self.pauseStartPin, 2, self.startPauseInterrupt)


    def recordInterrupt(self, gpio, level, tick):
        if(level == 0):
            print("Pressed Record")
            if self.deleted == 1:
                print("Record")
                self.deleted = 0
                self.oscClient.send_message("/sl/" + str(self.number) + "/hit", "record")
            else:
                if self.status == 2:
                    self.oscClient.send_message("/sl/" + str(self.number) + "/hit", "record")
                elif self.status == 4:
                    self.oscClient.send_message("/sl/" + str(self.number) + "/hit", "overdub")
                elif self.status == 5:
                    self.oscClient.send_message("/sl/" + str(self.number) + "/hit", "overdub")


    def startPauseInterrupt(self, gpio, level, tick):
        if level == 0:
            # if self.status == 10:
            #     noonePlaying = True
            #     for loop in self.sooperlooper.loops:
            #         if loop.status == 4:
            #             noonePlaying = False
            #     if noonePlaying:
            #         self.oscClient.send_message("/sl/" + str(self.number) + "/hit", "trigger")
            # else:
            self.oscClient.send_message("/sl/" + str(self.number) + "/hit", "mute")
            self.pausePressTime = time.clock()
        elif level == 1:
            releaseTime = time.clock()
            pressedTime = releaseTime - self.pausePressTime
            print(str(pressedTime))
            if pressedTime >= 0.25:
                self.deleted = 1
                if self.status != 10:
                    self.oscClient.send_message("/sl/" + str(self.number) + "/hit", "mute")
                self.updateRGBRing()
            elif pressedTime >= 0.08:
                self.oscClient.send_message("/sl/" + str(self.number) + "/hit", "undo")

    def mute(self):
        if self.status != 10 and self.deleted != 1:
            self.oscClient.send_message("/sl/" + str(self.number) + "/hit", "mute")

    def triggerStart(self):
        if self.status == 10:
            print("start")
            self.oscClient.send_message("/sl/" + str(self.number) + "/hit", "trigger")

    def setLoopPos(self, value):
        self.loopPos = value
        if self.status == 4 or self.status == 5:
            self.updateRGBRing()

    def setLoopLen(self, value):
        self.loopLen = value
        if self.status == 4 or self.status == 5:
            self.updateRGBRing()

    def setLoopStatus(self, value):
        if value != self.status:
            self.status = value
            self.updateRGBRing()

    def updateRGBRing(self):
        self.ring.clear()
        if self.deleted == 1:
            pass
        elif self.status == 4:
            if self.loopLen != 0:
                onLedCount = int(round(self.loopPos / self.loopLen * self.ring.LED_COUNT,1))
                for i in range(onLedCount):
                    self.ring.strip.setLED((self.number * self.ring.LED_COUNT + i), 0, 255, 0)
        elif self.status == 5:
            if self.loopLen != 0:
                onLedCount = int(round(self.loopPos / self.loopLen * self.ring.LED_COUNT, 1))
                for i in range(onLedCount):
                    self.ring.strip.setLED((self.number * self.ring.LED_COUNT + i), 255, 0, 0)
        elif self.status == 2:
            self.ring.setColor(255, 0, 0)
        elif self.status == 10:
            self.ring.setColor(255, 255, 0)
        elif self.status == 1:
            self.ring.setColor(0, 0, 255)
        elif self.status == 3:
            self.ring.setColor(0, 0, 255)
        self.ring.strip.show()

    def getStatus(self):
        self.oscClient.send_message("/sl/"+str(self.number)+"/get",["state", "192.168.1.2:9952", "/statusChanged"])

    def reset(self):
        self.deleted = 1
        self.updateRGBRing()