import subprocess
import time

class Jack:
    def start(self):
        print("Killing all jacks")
        #subprocess.run(["killall jackd"], shell=True)
        #time.sleep(1)
        print("Starting new jack")
        #subprocess.Popen(["/usr/bin/jackd -P95 -dalsa -r48000 -p512 -n2 -s -H -M -D -Chw:U192k -Phw:U192k"], shell=True)
        print("waiting for jack")
        #time.sleep(2)