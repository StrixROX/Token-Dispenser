#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

# For Futaba S3003 Servo

PWM=32 # pin number of PWM pin being used

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PWM, GPIO.OUT)

freq = 50.0 # PWM frequency
servo = GPIO.PWM(PWM,freq)

# after accounting for error
dc_min = 3.35
dc_neut = 7.5
dc_max = 11.8

servo.start(dc_neut)
print("Servo set to neutral position.")
print("Waiting for 1 second")
time.sleep(1)

def cleanup():
    print("Cleaning up")
    servo.stop()
    GPIO.cleanup()
    print("Cleanup complete")

def set_servo_angle(deg):
    deg = min(max(deg - 90, -90), 90) # limiting value between -90 and 90

    # this style of code allows us to use different
    # slopes for interpolating intermediate duty cycle values
    d1 = dc_neut - dc_min
    d2 = dc_max - dc_neut

    if deg == -90:
        servo.ChangeDutyCycle(dc_min)
    elif deg == 0:
        servo.ChangeDutyCycle(dc_neut)
    elif deg == 90:
        servo.ChangeDutyCycle(dc_max)
    elif deg < 0:
        servo.ChangeDutyCycle(dc_neut + (deg / 90) * d2)
    elif deg > 0:
        servo.ChangeDutyCycle(dc_neut + (deg / 90) * d2)

try:
    while True:
        val = float(input("Enter angle (0 to 180): "))
        set_servo_angle(val)

except Exception:
    cleanup()

cleanup()