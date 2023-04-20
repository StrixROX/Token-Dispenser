#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

'''
### For Futaba S3003 Servo

PWM=32 # pin number of PWM pin being used
freq = 50.0 # PWM frequency

# after accounting for error
dc_min = 3.30
dc_neut = 7.45
dc_max = 11.80
'''

class ServoController:
    def __init__(self, PWM:int, freq:int, dc_min:float, dc_neut:float, dc_max:float):
        self.PWM = PWM
        self.freq = freq
        self.dc_min = dc_min
        self.dc_neut = dc_neut
        self.dc_max = dc_max

    def init(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.PWM, GPIO.OUT)

        self.servo = GPIO.PWM(self.PWM, self.freq)
        self.servo.start(self.dc_neut)
        print("Servo set to neutral position.")
        print("Waiting for 1 second")
        time.sleep(1)

    def cleanup(self):
        print("Cleaning up...")
        self.servo.stop()
        GPIO.cleanup()
        print("Cleanup complete.")

    def setAngle(self, deg:float):
        deg = min(max(deg - 90, -90), 90) # limiting value between -90 and 90

        # this style of code allows us to use different
        # slopes for interpolating intermediate duty cycle values
        d1 = self.dc_neut - self.dc_min
        d2 = self.dc_max - self.dc_neut

        if deg == -90:
            self.servo.ChangeDutyCycle(self.dc_min)
        elif deg == 0:
            self.servo.ChangeDutyCycle(self.dc_neut)
        elif deg == 90:
            self.servo.ChangeDutyCycle(self.dc_max)
        elif deg < 0:
            self.servo.ChangeDutyCycle(self.dc_neut + (deg / 90) * d2)
        elif deg > 0:
            self.servo.ChangeDutyCycle(self.dc_neut + (deg / 90) * d2)