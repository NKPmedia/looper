import pigpio
from loop import Loop
import time
from ledrgbstrip import LedRGBStrip
from SooperLooper import SooperLooper
from jack import Jack
import subprocess
from I2C_LCD_driver import lcd
from bootscreen import BootScreen
from pythonosc import udp_client
from oscserer import OscServer

print("Starting Rasp-Looper Interface")

subprocess.Popen(["pigpiod"])

piGpio = pigpio.pi()

lcd = lcd()
bootscreen = BootScreen(lcd)
bootscreen.write("Starting UI")
strip = LedRGBStrip()
strip.init()
strip.testStrip()

bootscreen.write("Starting Jack")
jack = Jack()
jack.start()

bootscreen.write("Starting Looper")
sooperlooper = SooperLooper()
sooperlooper.start()

client = udp_client.SimpleUDPClient("192.168.0.1", 9951)

sooperlooper.creatLoops(strip, client, piGpio)
sooperlooper.setDefaultValues(client)

time.sleep(1)
bootscreen.write("Waiting for reset")
sooperlooper.resetLoops()

bootscreen.write("Ready :D", "Enjoy looping")
print("Interface started")
print("Starting to collect data")

oscServer = OscServer();
oscServer.connect(client, sooperlooper.loops)