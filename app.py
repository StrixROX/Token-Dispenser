import Servo
import time

myServo = Servo(PWM=32, freq=50, dc_min=3.30, dc_neut=7.45, dc_max=11.80)
myServo.init()

# servo testing code
myServo.setAngle(0)
time.sleep(1)
myServo.setAngle(90)
time.sleep(1)
myServo.setAngle(180)
time.sleep(1)
myServo.setAngle(90)
time.sleep(1)
myServo.setAngle(0)
time.sleep(1)

myServo.cleanup()