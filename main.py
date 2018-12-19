import pigpio
import time
from ledrgbstrip import LedRGBStrip
from SooperLooper import SooperLooper
import subprocess
from I2C_LCD_driver import lcd
from bootscreen import BootScreen
from pythonosc import udp_client
from oscserer import OscServer

lcd = lcd()
bootscreen = BootScreen(lcd)

bootscreen.write("Starting...", "Rpi-Looper")
print("Starting Rasp-Looper Interface")

subprocess.Popen(["pigpiod"])

time.sleep(2)

piGpio = pigpio.pi()


bootscreen.write("Starting UI")
strip = LedRGBStrip()
strip.init()
strip.testStrip()

client = udp_client.SimpleUDPClient("192.168.1.1", 9951)



sooperlooper = SooperLooper()
bootscreen.write("Starting Looper")
sooperlooper.start()



sooperlooper.creatLoops(strip, client, piGpio)
sooperlooper.setDefaultValues(client)

time.sleep(1)
bootscreen.write("Waiting for reset")
sooperlooper.resetLoops()

bootscreen.write("Ready :D", "Enjoy looping")
print("Interface started")
print("Starting to collect data")

oscServer = OscServer()
oscServer.connect(client, sooperlooper.loops)