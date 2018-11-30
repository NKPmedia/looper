import subprocess
import time

class KlickMetro:


    def start(self):
        print("Killing all jacks")
        subprocess.run(["killall klick"], shell=True)
        print("Starting new klick")
        subprocess.Popen(["klick"], shell=True)
        print("waiting for klick")
        time.sleep(1)