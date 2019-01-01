#!/usr/bin/env python3

from time import sleep

from ev3dev2.motor import MediumMotor, LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent
from ev3dev2.sensor.lego import TouchSensor

touch_start_button = TouchSensor()
motor_conveyor = LargeMotor(OUTPUT_A)
motor_fan = LargeMotor(OUTPUT_B)
motor_water = MediumMotor(OUTPUT_C)

while True:
    touch_start_button.wait_for_pressed()
    motor_conveyor.on(SpeedPercent(8))
    sleep(1)
    motor_water.on_for_rotations(SpeedPercent(10), 0.5)
    sleep(1.5)
    motor_water.on_for_rotations(SpeedPercent(10), -0.5)
    sleep(1.5)
    motor_fan.on(SpeedPercent(100))
    motor_conveyor.on(SpeedPercent(3))
    sleep(4)
    motor_fan.off()
    motor_conveyor.off()
