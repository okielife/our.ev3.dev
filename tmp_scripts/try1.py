#!/usr/bin/env python3

from ev3dev2.motor import LargeMotor, OUTPUT_A, SpeedPercent
from ev3dev2.sensor.lego import TouchSensor

m = LargeMotor(OUTPUT_A)

m.on(SpeedPercent(50))
m.off()

