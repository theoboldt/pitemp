#!/usr/bin/python

import sensor
import lcd
import csv

import time
import os
import datetime
import sys
import re
import circular_buffer

lcd.init()

last_time = datetime.datetime.now()
last_minute = last_time.minute
probe_minute_01 = circular_buffer.CircularBuffer(size=30)
probe_minute_15 = circular_buffer.CircularBuffer(size=15)
probes_minute_30 = circular_buffer.CircularBuffer(size=30)
probes_minute_60 = circular_buffer.CircularBuffer(size=60)

# initialize buffers
current_temperature = sensor.read()
probe_minute_01.append(current_temperature)
probe_minute_15.append(current_temperature)
probes_minute_30.append(current_temperature)
probes_minute_60.append(current_temperature)

while True:
    try:
        current_time = datetime.datetime.now()
        current_minute = current_time.minute
        current_temperature = sensor.read()

        probe_minute_01.append(current_temperature)

        lcd.top("{:2.1f}".format(current_temperature) + chr(223) + "C  " + current_time.strftime("%H:%M:%S"))

        if last_minute != current_minute:
            probe_minute_15.append(current_temperature)
            probes_minute_30.append(current_temperature)
            probes_minute_60.append(current_temperature)
            csv.append(current_time.strftime("%s") + ";" + current_time.isoformat() + ";" + "{:2.1f}".format(
                current_temperature).replace('.', ',') + "\n")

        lcd.bottom("{:2.1f}".format(probes_minute_60.average) + chr(223) + " " + "{:2.1f}".format(
            probes_minute_30.average) + chr(223) + " " + "{:2.1f}".format(probe_minute_15.average) + chr(223))

        time.sleep(2)

        last_minute = current_minute
        last_time = current_time

    except KeyboardInterrupt:
        lcd.cleanup()
        sys.exit(0)
