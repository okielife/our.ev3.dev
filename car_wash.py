#!/usr/bin/env python3

from time import sleep

from ev3dev2.motor import MediumMotor, LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.sound import Sound
from ev3dev2.led import Leds

print("Python initialized")

touch_start_button = TouchSensor()
motor_conveyor = LargeMotor(OUTPUT_A)
motor_fan = LargeMotor(OUTPUT_B)
motor_water = MediumMotor(OUTPUT_C)
sound = Sound()
leds = Leds()

# change voice options here
speak_options = '-a 200 -s 130 -v en+f3'

# clear it if it was already running
motor_conveyor.off()
motor_fan.off()
motor_water.off()

# announnce car wash is ready for use
print("Got motors and sensors connected.")
sound.speak("Car wash ready", espeak_opts=speak_options)

# sit and wait forever for a car to enter the wash
while True:
    leds.set_color("LEFT", "GREEN")
    leds.set_color("RIGHT", "GREEN")
    print("Waiting for car...")
    touch_start_button.wait_for_pressed()
    print("Car wash button pressed, ready for entry")
    leds.set_color("LEFT", "YELLOW")
    leds.set_color("RIGHT", "YELLOW")
    sound.speak("Please drive onto conveyor and roll up your windows!", espeak_opts=speak_options)
    print("Car entering car wash...")
    leds.set_color("LEFT", "RED")
    leds.set_color("RIGHT", "RED")
    motor_conveyor.on(SpeedPercent(8))
    sleep(1)
    print(" Pouring water")
    motor_water.on_for_rotations(SpeedPercent(10), 0.5)
    sleep(1.5)
    motor_water.on_for_rotations(SpeedPercent(10), -0.5)
    sleep(1.5)
    print(" Drying car")
    motor_fan.on(SpeedPercent(100))
    motor_conveyor.on(SpeedPercent(3))
    sleep(4)
    print(" Done")
    motor_fan.off()
    motor_conveyor.off()
    sound.speak("Thank you for coming to the Hot Wheels Car Wash!", espeak_opts=speak_options)

