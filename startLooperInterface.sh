#!/usr/bin/env bash

export DISPLAY=:0

# dbus-launch started, DBUS_SESSION_BUS_ADDRESS exported:
export `dbus-launch | grep ADDRESS`

# dbus-launch started, DBUS_SESSION_BUS_PID exported
export `dbus-launch | grep PID`
# (4) Start Jack

/usr/bin/jackd -P95 --realtime -dalsa -r48000 -p128 -n2 -s -D -Chw:U192k -Phw:U192k &


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

