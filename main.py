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
probes_one_minute = circular_buffer.CircularBuffer(size=30)
probes_five_minutes = circular_buffer.CircularBuffer(size=5)
probes_fifteen_minutes = circular_buffer.CircularBuffer(size=15)
probes_thirty_minutes = circular_buffer.CircularBuffer(size=30)

# initialize buffers
current_temperature = sensor.read()
probes_one_minute.append(current_temperature)
probes_five_minutes.append(current_temperature)
probes_fifteen_minutes.append(current_temperature)
probes_thirty_minutes.append(current_temperature)

while True:
    try:
        current_time = datetime.datetime.now()
        current_minute = current_time.minute
        current_temperature = sensor.read()

        probes_one_minute.append(current_temperature)

        lcd.top("{:2.1f}".format(current_temperature) + chr(223) + "C  " + current_time.strftime("%H:%M:%S"))

        if last_minute != current_minute:
            probes_five_minutes.append(current_temperature)
            probes_fifteen_minutes.append(current_temperature)
            probes_thirty_minutes.append(current_temperature)
            csv.append(current_time.strftime("%s") + ";" + str(current_temperature))

        lcd.bottom("{:2.1f}".format(probes_thirty_minutes.average) + chr(223) + " " + "{:2.1f}".format(
            probes_fifteen_minutes.average) + chr(223) + " " + "{:2.1f}".format(probes_five_minutes.average) + chr(223))

        time.sleep(2)

        last_minute = current_minute
        last_time = current_time

    except KeyboardInterrupt:
        lcd.cleanup()
