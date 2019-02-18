#!/usr/bin/env python3
from ev3dev2.motor import OUTPUT_A, SpeedPercent, LargeMotor
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.sensor import INPUT_1
from random import randint

wheel_motor = LargeMotor(OUTPUT_A)
start_button = TouchSensor(INPUT_1)

speed_dictionary = [
    (0.1, 25),
    (0.1, 50),
    (0.1, 75),
    (1, 100),
    (1, 75),
    (1, 50),
    (1, 25),
    (1, 10)
]

while True:
    start_button.wait_for_pressed()
    multiplier = float(randint(75, 125)) / 100.0
    for speed_info in speed_dictionary:
        time_to_run = speed_info[0] * multiplier
        wheel_motor.on_for_seconds(SpeedPercent(speed_info[1]), time_to_run)
    wheel_motor.off()
