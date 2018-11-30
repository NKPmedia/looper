#!/usr/bin/env bash

sooperlooper -l 3 -c 1 &
pigpiod
#klick -P -T -o9953&
sleep 1

jack_connect system:capture_1 sooperlooper:common_in_1
jack_connect system:capture_2 sooperlooper:common_in_2

jack_connect system:playback_1 sooperlooper:common_out_1
jack_connect system:playback_2 sooperlooper:common_out_2

jack_connect system:playback_1 klick:out
jack_connect system:playback_2 klick:out
sleep 1
/usr/bin/python3 /home/pi/looper/main.py&