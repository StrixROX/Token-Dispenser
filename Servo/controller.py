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
    def __init__(self, PWM:int, freq:int, dc_min:float, dc_neut:float, dc_max:float) -> None:
        self.PWM = PWM
        self.freq = freq
        self.dc_min = dc_min
        self.dc_neut = dc_neut
        self.dc_max = dc_max

        self.is_ready = False
        self.position = None # always from -90 to 90, both inclusive

    def init(self) -> None:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.PWM, GPIO.OUT)

        self.servo = GPIO.PWM(self.PWM, self.freq)
        self.servo.start(self.dc_neut)
        print("Servo ready.")
        print("Servo set to neutral position.")
        print("Waiting for 1 second...")
        time.sleep(1)
        
        self.is_ready = True
        self.position = 0

    def cleanup(self) -> None:
        print("Cleaning up...")
        self.servo.stop()
        GPIO.cleanup()
        print("Cleanup complete.")

        self.is_ready = False

    def setAngle(self, deg:float, mode:int = 1) -> None:
        # mode 1: deg input is from 0 to 180
        # mode 2: deg input is from -90 to 90
        
        if mode == 1:
            if deg < 0 or deg > 180:
                raise ValueError("Mode=1: Input angle should be between 0 and 180, both inclusive.")
            pos = deg - 90
        elif mode == 2:
            if deg < -90 or deg > 90:
                raise ValueError("Mode=2: Input angle should be between -90 and 90, both inclusive.")
            pos = deg

        pos = min(max(pos, -90), 90) # limiting value between -90 and 90

        # this style of code allows us to use different
        # slopes for interpolating intermediate duty cycle values
        d1 = self.dc_neut - self.dc_min
        d2 = self.dc_max - self.dc_neut

        if pos == -90:
            self.servo.ChangeDutyCycle(self.dc_min)
        elif pos == 0:
            self.servo.ChangeDutyCycle(self.dc_neut)
        elif pos == 90:
            self.servo.ChangeDutyCycle(self.dc_max)
        elif pos < 0:
            self.servo.ChangeDutyCycle(self.dc_neut + (pos / 90) * d2)
        elif pos > 0:
            self.servo.ChangeDutyCycle(self.dc_neut + (pos / 90) * d2)
        
        self.position = pos