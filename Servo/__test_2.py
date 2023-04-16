from .controller import ServoController as Servo
import time

servo = Servo(PWM=32, freq=50, dc_min=3.30, dc_neut=7.45, dc_max=11.80)
servo.init()

try:
  while True:
    angle = float(input("Enter target angle (0 to 180): "))
    servo.setAngle(angle)
    time.sleep(1)

except Exception:
  servo.cleanup()